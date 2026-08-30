import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / "bin" / "psync"


class PsyncTests(unittest.TestCase):
    def run_status(self, manifest: str, *, strict: bool):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            projects = root / "projects"
            projects.mkdir()
            manifest_path = root / "projects.manifest"
            manifest_path.write_text(manifest, encoding="utf-8")
            environment = {
                **os.environ,
                "PROJECTS_DIR": str(projects),
                "PSYNC_MANIFEST": str(manifest_path),
                "PSYNC_MACHINE": "imac",
                "PSYNC_STRICT": "1" if strict else "0",
            }
            return subprocess.run(
                [str(SCRIPT), "status"],
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

    def test_status_remains_advisory_by_default(self):
        result = self.run_status(
            "sample\tgit@github.com:miniminjae92/sample.git\tall\n", strict=False
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("clone 필요", result.stdout)

    def test_strict_status_fails_for_unsynchronised_projects(self):
        result = self.run_status(
            "sample\tgit@github.com:miniminjae92/sample.git\tall\n", strict=True
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("clone 필요", result.stdout)


if __name__ == "__main__":
    unittest.main()
