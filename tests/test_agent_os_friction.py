import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "bin" / "agent-os-friction"
NOTE_RELPATH = Path("00 Inbox") / "생산성 불편일기.md"
NOTE_TEMPLATE = "# 생산성 불편일기\n\n## 미처리\n\n## 검토 완료\n"


class AgentOsFrictionTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.vault = self.root / "vault"
        self.note = self.vault / NOTE_RELPATH
        self.note.parent.mkdir(parents=True)
        self.note.write_text(NOTE_TEMPLATE, encoding="utf-8")
        self.addCleanup(self._tmp.cleanup)

    def run_friction(self, *args):
        env = os.environ.copy()
        env["DEVELOPER_OS_VAULT"] = str(self.vault)
        env["PATH"] = os.defpath  # ops-event 등 부수효과를 차단한다
        return subprocess.run(
            [str(SCRIPT), *args],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def entries(self):
        body = self.note.read_text(encoding="utf-8")
        return [line for line in body.splitlines() if line.startswith("- [ ]")]

    def test_help_prints_usage_without_recording_friction(self):
        for flag in ("--help", "-h"):
            with self.subTest(flag=flag):
                self.note.write_text(NOTE_TEMPLATE, encoding="utf-8")

                result = self.run_friction(flag)

                self.assertEqual(result.returncode, 0)
                self.assertIn("usage: agent-os-friction", result.stdout)
                self.assertEqual(self.entries(), [])

    def test_help_flag_inside_message_is_still_recorded(self):
        # 이 버그를 기록하려면 메시지 안에 --help 가 들어가야 한다. 첫 인자만
        # 도움말로 해석해야 그 기록이 사라지지 않는다.
        result = self.run_friction("agent-os-friction --help가 도움말을 안 낸다")

        self.assertEqual(result.returncode, 0)
        recorded = self.entries()
        self.assertEqual(len(recorded), 1)
        self.assertIn("--help가 도움말을 안 낸다", recorded[0])

    def test_missing_message_is_an_error_not_a_help_request(self):
        result = self.run_friction()

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.entries(), [])

    def test_records_origin_and_message(self):
        result = self.run_friction("--origin", "agent", "escalation: worker→planner")

        self.assertEqual(result.returncode, 0)
        recorded = self.entries()
        self.assertEqual(len(recorded), 1)
        self.assertIn("origin:agent", recorded[0])
        self.assertIn("escalation: worker→planner", recorded[0])


if __name__ == "__main__":
    unittest.main()
