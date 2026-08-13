import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "bin" / "agent-os-review-due"


class AgentOsReviewDueTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name) / "vault"
        self.runs = self.vault / "40 Reviews" / "Runs"
        self.periodic = self.vault / "40 Reviews" / "Periodic"
        self.runs.mkdir(parents=True)
        self.periodic.mkdir(parents=True)
        self.addCleanup(self._tmp.cleanup)

    def write(self, directory, name, body="", mtime=None):
        path = directory / name
        path.write_text(body, encoding="utf-8")
        if mtime is not None:
            os.utime(path, (mtime, mtime))
        return path

    def run_due(self, **env_overrides):
        env = os.environ.copy()
        env["DEVELOPER_OS_VAULT"] = str(self.vault)
        env["PATH"] = os.defpath  # ops-event 부수효과 차단
        env.update({k: str(v) for k, v in env_overrides.items()})
        result = subprocess.run(
            [str(SCRIPT)], text=True, capture_output=True, env=env, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_lists_unreviewed_run_filenames_not_just_the_count(self):
        # 개수만 있으면 어느 Run 이 미검토인지 mtime 을 손으로 대조해야 했다.
        now = time.time()
        self.write(self.periodic, "2026-08-01-review.md", mtime=now - 400)
        self.write(self.runs, "2026-07-20-old-run.md", mtime=now - 500)
        self.write(self.runs, "2026-08-05-b-run.md", mtime=now - 200)
        self.write(self.runs, "2026-08-03-a-run.md", mtime=now - 100)

        report = self.run_due()

        self.assertEqual(report["unreviewed_runs"], 2)
        self.assertEqual(
            report["unreviewed_run_files"],
            ["2026-08-03-a-run.md", "2026-08-05-b-run.md"],
        )

    def test_run_filenames_are_sorted_so_oldest_is_reviewed_first(self):
        now = time.time()
        self.write(self.periodic, "2026-08-01-review.md", mtime=now - 400)
        for name in ("2026-08-09-c.md", "2026-08-02-a.md", "2026-08-06-b.md"):
            self.write(self.runs, name, mtime=now - 100)

        report = self.run_due()

        self.assertEqual(
            report["unreviewed_run_files"],
            ["2026-08-02-a.md", "2026-08-06-b.md", "2026-08-09-c.md"],
        )

    def test_readme_is_not_counted_as_a_run(self):
        now = time.time()
        self.write(self.periodic, "2026-08-01-review.md", mtime=now - 400)
        self.write(self.runs, "README.md", mtime=now - 100)

        report = self.run_due()

        self.assertEqual(report["unreviewed_runs"], 0)
        self.assertEqual(report["unreviewed_run_files"], [])

    def test_file_list_stays_consistent_with_the_immediate_incident_list(self):
        now = time.time()
        self.write(self.periodic, "2026-08-01-review.md", mtime=now - 400)
        self.write(
            self.runs,
            "2026-08-04-incident.md",
            body="accepted_success: false\n",
            mtime=now - 100,
        )

        report = self.run_due()

        self.assertIn("immediate_incident", report["reasons"])
        self.assertEqual(report["immediate_runs"], ["2026-08-04-incident.md"])
        self.assertEqual(report["unreviewed_run_files"], ["2026-08-04-incident.md"])


if __name__ == "__main__":
    unittest.main()
