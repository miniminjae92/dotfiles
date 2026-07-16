import importlib.machinery
import importlib.util
import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "git-plan-ai"
LOADER = importlib.machinery.SourceFileLoader("git_plan_ai", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
git_plan_ai = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(git_plan_ai)


def run_git(repo: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", *arguments],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


class GitPlanAiTest(unittest.TestCase):
    def make_repository(self, root: Path) -> None:
        run_git(root, "init", "-q")
        run_git(root, "config", "user.name", "Test User")
        run_git(root, "config", "user.email", "test@example.com")
        (root / "tracked.txt").write_text("before\n", encoding="utf-8")
        run_git(root, "add", "tracked.txt")
        run_git(root, "commit", "-qm", "initial")

    def test_collects_staged_unstaged_and_untracked_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            self.make_repository(repo)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            (repo / "staged.txt").write_text("staged\n", encoding="utf-8")
            run_git(repo, "add", "staged.txt")
            (repo / "untracked.txt").write_text("TOP_SECRET\n", encoding="utf-8")

            changes = git_plan_ai.collect_repository_changes(repo)
            prompt = git_plan_ai.build_prompt(changes, max_diff_chars=6_000)

            self.assertEqual(
                set(changes.paths), {"tracked.txt", "staged.txt", "untracked.txt"}
            )
            self.assertIn("staged.txt", prompt)
            self.assertIn("tracked.txt", prompt)
            self.assertIn("untracked.txt", prompt)
            self.assertNotIn("TOP_SECRET", prompt)

    def test_truncates_diff_input(self):
        changes = git_plan_ai.ChangeSet(
            paths=("tracked.txt",),
            status=" M tracked.txt",
            staged_stat="",
            unstaged_stat="tracked.txt | 1 +",
            staged_name_status="",
            unstaged_name_status="M\ttracked.txt",
            staged_diff="",
            unstaged_diff="x" * 100,
            untracked=(),
        )

        prompt = git_plan_ai.build_prompt(changes, max_diff_chars=20)

        self.assertIn("[diff truncated at 20 characters]", prompt)
        self.assertNotIn("x" * 21, prompt)

    def test_validates_complete_plan_and_adds_stage_commands(self):
        plan = {
            "commits": [
                {
                    "purpose": "기능 추가",
                    "files": ["tracked.txt", "file with space.txt"],
                    "message": "feat(core): 기능 추가",
                    "reason": "같은 기능 변경",
                }
            ],
            "warnings": [],
        }

        result = git_plan_ai.validate_plan(
            plan, ("tracked.txt", "file with space.txt")
        )

        self.assertEqual(
            result["commits"][0]["stage_command"],
            "git add -A -- tracked.txt 'file with space.txt'",
        )

    def test_rejects_incomplete_plan(self):
        plan = {
            "commits": [
                {
                    "purpose": "기능 추가",
                    "files": ["tracked.txt"],
                    "message": "feat(core): 기능 추가",
                    "reason": "같은 기능 변경",
                }
            ],
            "warnings": [],
        }

        with self.assertRaises(git_plan_ai.GitPlanError):
            git_plan_ai.validate_plan(plan, ("tracked.txt", "missing.txt"))

    def test_compact_is_default_and_full_is_the_only_size_override(self):
        compact = git_plan_ai.build_parser().parse_args([])
        full = git_plan_ai.build_parser().parse_args(["--full"])

        self.assertFalse(compact.full)
        self.assertTrue(full.full)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            git_plan_ai.build_parser().parse_args(["--compact"])

    def test_detects_sensitive_paths_before_cloud_delegation(self):
        self.assertEqual(
            git_plan_ai.sensitive_paths(("src/app.py", ".env", "certs/server.pem")),
            [".env", "certs/server.pem"],
        )

    @mock.patch.object(git_plan_ai.shutil, "which", return_value="/fake/agy")
    @mock.patch.object(git_plan_ai.subprocess, "run")
    def test_runs_agy_in_plan_mode_and_empty_directory(self, run, _which):
        response = {
            "commits": [
                {
                    "purpose": "기능 추가",
                    "files": ["tracked.txt"],
                    "message": "feat(core): 기능 추가",
                    "reason": "단일 변경",
                }
            ],
            "warnings": [],
        }
        run.return_value = subprocess.CompletedProcess(
            ["agy"], 0, stdout=f"```json\n{json.dumps(response)}\n```", stderr=""
        )

        result = git_plan_ai.run_agy("prompt", model="test-model")

        self.assertEqual(result, response)
        command = run.call_args.args[0]
        self.assertEqual(command[0], "agy")
        self.assertIn("--mode", command)
        self.assertIn("plan", command)
        self.assertIn("--sandbox", command)
        self.assertIn("--print-timeout", command)
        self.assertNotEqual(Path(run.call_args.kwargs["cwd"]), Path.cwd())

    @mock.patch.object(git_plan_ai, "run_agy")
    def test_main_returns_validated_plan_without_writing_git(self, run_agy):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            self.make_repository(repo)
            (repo / "tracked.txt").write_text("after\n", encoding="utf-8")
            run_agy.return_value = {
                "commits": [
                    {
                        "purpose": "추적 파일 수정",
                        "files": ["tracked.txt"],
                        "message": "fix(core): 추적 파일 내용 수정",
                        "reason": "단일 파일 변경",
                    }
                ],
                "warnings": [],
            }

            with mock.patch.object(git_plan_ai, "repository_root", return_value=repo):
                self.assertEqual(git_plan_ai.main([]), 0)

            self.assertEqual(
                run_git_output(repo, "status", "--short"), " M tracked.txt"
            )


def run_git_output(repo: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.rstrip("\n")


if __name__ == "__main__":
    unittest.main()
