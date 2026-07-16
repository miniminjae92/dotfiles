import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "lazygit-ai-commit"
REGISTRY_PATH = Path(__file__).parents[1] / "ai-tools" / "models.json"
CONVENTION_PATH = (
    Path(__file__).parents[1] / "conventions" / "commit-message" / "korean-angularjs.md"
)


def run_git(repo: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", *arguments],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


class LazygitAiCommitTest(unittest.TestCase):
    def make_repository(self, root: Path) -> None:
        run_git(root, "init", "-q")
        run_git(root, "config", "user.name", "Test User")
        run_git(root, "config", "user.email", "test@example.com")
        (root / "feature.txt").write_text("before\n", encoding="utf-8")
        run_git(root, "add", "feature.txt")
        run_git(root, "commit", "-qm", "initial")
        (root / "feature.txt").write_text("after\n", encoding="utf-8")
        run_git(root, "add", "feature.txt")

    def make_fake_commands(self, directory: Path) -> None:
        agy = directory / "agy"
        agy.write_text(
            """#!/usr/bin/env python3
import os
import sys
from pathlib import Path

prompt = sys.argv[sys.argv.index("-p") + 1]
Path(os.environ["PROMPT_CAPTURE"]).write_text(prompt, encoding="utf-8")
Path(os.environ["MODEL_CAPTURE"]).write_text(
    sys.argv[sys.argv.index("--model") + 1], encoding="utf-8"
)
print("feat(core): 기능 추가")
""",
            encoding="utf-8",
        )
        agy.chmod(0o755)
        pbcopy = directory / "pbcopy"
        pbcopy.write_text("#!/bin/sh\ncat >/dev/null\n", encoding="utf-8")
        pbcopy.chmod(0o755)

    def run_script(self, repo: Path, fake_bin: Path, *arguments: str) -> str:
        environment = dict(os.environ)
        environment.update(
            {
                "PATH": f"{fake_bin}:{environment['PATH']}",
                "PROMPT_CAPTURE": str(repo / "prompt.txt"),
                "MODEL_CAPTURE": str(repo / "model.txt"),
                "AI_MODEL_REGISTRY": str(REGISTRY_PATH),
                "LAZYGIT_AI_COMMIT_CONVENTION": str(CONVENTION_PATH),
            }
        )
        result = subprocess.run(
            [str(SCRIPT_PATH), "agy", *arguments],
            cwd=repo,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return (repo / "prompt.txt").read_text(encoding="utf-8")

    def test_compact_prompt_is_default_and_model_comes_from_registry(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            fake_bin = root / "bin"
            repo.mkdir()
            fake_bin.mkdir()
            self.make_repository(repo)
            self.make_fake_commands(fake_bin)

            prompt = self.run_script(repo, fake_bin)

            self.assertIn("Staged summary:", prompt)
            self.assertIn("Changed files:", prompt)
            self.assertNotIn("Convention:", prompt)
            self.assertEqual(
                (repo / "model.txt").read_text(encoding="utf-8"),
                "Gemini 3.5 Flash (Low)",
            )

    def test_full_option_uses_full_convention_prompt(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            fake_bin = root / "bin"
            repo.mkdir()
            fake_bin.mkdir()
            self.make_repository(repo)
            self.make_fake_commands(fake_bin)

            prompt = self.run_script(repo, fake_bin, "--full")

            self.assertIn("Convention:", prompt)
            self.assertNotIn("Staged summary:", prompt)


if __name__ == "__main__":
    unittest.main()
