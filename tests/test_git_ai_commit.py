import contextlib
import importlib.machinery
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "git-ai-commit"
LOADER = importlib.machinery.SourceFileLoader("git_ai_commit", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
git_ai_commit = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(git_ai_commit)


def git(repo: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


class GitAiCommitTest(unittest.TestCase):
    def make_repository(self, root: Path) -> None:
        git(root, "init", "-q")
        git(root, "config", "user.name", "Test User")
        git(root, "config", "user.email", "test@example.com")
        (root / "one.txt").write_text("before one\n", encoding="utf-8")
        (root / "two.txt").write_text("before two\n", encoding="utf-8")
        git(root, "add", ".")
        git(root, "commit", "-qm", "initial")

    def plan(self, repo: Path, *, warnings: list[str] | None = None) -> dict:
        return {
            "provider": "agy",
            "model": "Gemini test",
            "mode": "compact",
            "changed_files": 2,
            "commits": [
                {
                    "purpose": "첫 변경",
                    "files": ["one.txt"],
                    "message": "feat(one): 첫 변경",
                    "reason": "독립 변경",
                    "stage_command": "git add -A -- one.txt",
                },
                {
                    "purpose": "둘째 변경",
                    "files": ["two.txt"],
                    "message": "fix(two): 둘째 변경",
                    "reason": "독립 변경",
                    "stage_command": "git add -A -- two.txt",
                },
            ],
            "warnings": warnings or [],
        }

    def prepare_changes(self, repo: Path) -> None:
        (repo / "one.txt").write_text("after one\n", encoding="utf-8")
        (repo / "two.txt").write_text("after two\n", encoding="utf-8")

    def save_plan(self, repo: Path, *, warnings: list[str] | None = None) -> None:
        git_ai_commit.save_cache(
            repo,
            self.plan(repo, warnings=warnings),
            git_ai_commit.worktree_fingerprint(repo),
        )

    def test_dry_run_validates_without_changing_repository(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            self.make_repository(repo)
            self.prepare_changes(repo)
            self.save_plan(repo)
            before = git_ai_commit.worktree_fingerprint(repo)

            with contextlib.redirect_stdout(io.StringIO()):
                result = git_ai_commit.apply_plan(
                    repo, reviewed=False, dry_run=True
                )

            self.assertEqual(result, 0)
            self.assertEqual(before, git_ai_commit.worktree_fingerprint(repo))
            self.assertEqual(git(repo, "rev-list", "--count", "HEAD"), "1")

    def test_apply_creates_commits_in_order_and_removes_cache(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            self.make_repository(repo)
            self.prepare_changes(repo)
            self.save_plan(repo)

            with contextlib.redirect_stdout(io.StringIO()):
                result = git_ai_commit.apply_plan(
                    repo, reviewed=False, dry_run=False
                )

            self.assertEqual(result, 0)
            self.assertEqual(git(repo, "status", "--short"), "")
            self.assertEqual(git(repo, "rev-list", "--count", "HEAD"), "3")
            self.assertEqual(
                git(repo, "log", "-2", "--pretty=%s").splitlines(),
                ["fix(two): 둘째 변경", "feat(one): 첫 변경"],
            )
            self.assertFalse(git_ai_commit.cache_path(repo).exists())

    def test_refuses_changed_worktree_after_plan(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            self.make_repository(repo)
            self.prepare_changes(repo)
            self.save_plan(repo)
            (repo / "one.txt").write_text("changed again\n", encoding="utf-8")

            with self.assertRaises(git_ai_commit.AiCommitError):
                git_ai_commit.apply_plan(repo, reviewed=False, dry_run=True)

    def test_dry_run_shows_warning_and_apply_requires_reviewed_flag(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            self.make_repository(repo)
            self.prepare_changes(repo)
            self.save_plan(repo, warnings=["검토 필요"])

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(
                    git_ai_commit.apply_plan(repo, reviewed=False, dry_run=True), 0
                )
            self.assertIn("검토 필요", output.getvalue())

            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(
                git_ai_commit.AiCommitError
            ):
                git_ai_commit.apply_plan(repo, reviewed=False, dry_run=False)

            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(
                    git_ai_commit.apply_plan(repo, reviewed=True, dry_run=False), 0
                )
            self.assertEqual(git(repo, "rev-list", "--count", "HEAD"), "3")

    def test_refuses_staged_files_outside_first_group(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            self.make_repository(repo)
            self.prepare_changes(repo)
            git(repo, "add", "two.txt")
            self.save_plan(repo)

            with self.assertRaises(git_ai_commit.AiCommitError):
                git_ai_commit.apply_plan(repo, reviewed=False, dry_run=True)

    @mock.patch.object(git_ai_commit, "create_plan", return_value=0)
    @mock.patch.object(git_ai_commit, "repository_root", return_value=Path("/repo"))
    def test_no_subcommand_defaults_to_compact_plan(self, _root, create_plan):
        self.assertEqual(git_ai_commit.main([]), 0)
        create_plan.assert_called_once_with(Path("/repo"), full=False)


if __name__ == "__main__":
    unittest.main()
