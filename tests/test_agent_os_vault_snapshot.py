import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "bin" / "agent-os-vault-snapshot"

GIT_ENV = {
    "GIT_AUTHOR_NAME": "test",
    "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "test",
    "GIT_COMMITTER_EMAIL": "test@example.com",
}


class AgentOsVaultSnapshotTest(unittest.TestCase):
    """pull 실패를 원인별로 갈라 보고하는지 확인한다.

    수정 전에는 오프라인이든 실행 중 편집이든 전부 'pull conflict, manual merge
    needed' 로 보고해서, 실제로는 정상인 볼트를 고장난 것으로 오진하게 만들었다.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def git(self, repo, *args):
        env = os.environ.copy()
        env.update(GIT_ENV)
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            text=True,
            capture_output=True,
            env=env,
            check=True,
        )

    def make_remote(self):
        remote = self.root / "remote.git"
        subprocess.run(
            ["git", "init", "--bare", "-q", "-b", "main", str(remote)], check=True
        )
        return remote

    def make_vault(self, name, remote=None):
        """원격과 1커밋을 공유하는 볼트를 만든다."""
        vault = self.root / name
        vault.mkdir()
        self.git(vault, "init", "-q", "-b", "main")
        (vault / "note.md").write_text("seed\n", encoding="utf-8")
        self.git(vault, "add", "-A")
        self.git(vault, "commit", "-q", "-m", "seed")
        if remote is not None:
            self.git(vault, "remote", "add", "origin", str(remote))
            self.git(vault, "push", "-q", "origin", "main")
        return vault

    def run_snapshot(self, vaults, extra_env=None):
        env = os.environ.copy()
        env.update(GIT_ENV)
        # 두 볼트 슬롯을 테스트용 경로로 고정한다. 실제 볼트는 건드리지 않는다.
        env["YGGDRASIL_VAULT"] = str(vaults[0])
        env["DEVELOPER_OS_VAULT"] = str(vaults[1] if len(vaults) > 1 else vaults[0])
        env["HOME"] = str(self.root / "home")
        env["PATH"] = f"/usr/bin:/bin:/usr/local/bin:{os.defpath}"
        env.update(extra_env or {})
        return subprocess.run(
            ["bash", str(SCRIPT)], text=True, capture_output=True, env=env, check=False
        )

    def test_diverged_history_that_conflicts_is_reported_as_needing_a_human(self):
        remote = self.make_remote()
        vault = self.make_vault("vault-a", remote)
        other = self.make_vault("vault-b")
        self.git(other, "remote", "add", "origin", str(remote))
        self.git(other, "fetch", "-q", "origin", "main")
        self.git(other, "reset", "-q", "--hard", "origin/main")

        # 같은 줄을 양쪽에서 다르게 고쳐 rebase 충돌을 만든다.
        (other / "note.md").write_text("from imac\n", encoding="utf-8")
        self.git(other, "commit", "-qam", "imac edit")
        self.git(other, "push", "-q", "origin", "main")
        (vault / "note.md").write_text("from macbook\n", encoding="utf-8")

        result = self.run_snapshot([vault])

        self.assertIn("manual check needed", result.stderr)
        self.assertNotIn("pull deferred", result.stderr)
        # git 이 실제로 한 말을 같이 남겨야 진단을 처음부터 다시 하지 않는다.
        self.assertIn("git:", result.stderr)
        # 무인 잡이 rebase 중간 상태를 남기면 다음 실행까지 연쇄로 깨진다.
        self.assertFalse((vault / ".git" / "rebase-merge").exists())
        self.assertFalse((vault / ".git" / "rebase-apply").exists())

    def test_unreachable_remote_is_reported_as_offline_not_as_a_conflict(self):
        vault = self.make_vault("vault-offline")
        self.git(
            vault, "remote", "add", "origin", "git@127.0.0.1:1/nonexistent-vault.git"
        )

        result = self.run_snapshot([vault])

        self.assertNotIn("manual check needed", result.stderr)
        self.assertNotIn("manual merge needed", result.stderr)
        self.assertIn("offline/auth", result.stderr)

    def test_local_commit_still_happens_so_history_is_never_lost(self):
        # push 나 pull 이 실패해도 로컬 커밋은 남아야 한다. 그게 이 잡의 본체다.
        vault = self.make_vault("vault-local")
        self.git(
            vault, "remote", "add", "origin", "git@127.0.0.1:1/nonexistent-vault.git"
        )
        (vault / "new-note.md").write_text("written while offline\n", encoding="utf-8")

        result = self.run_snapshot([vault])

        self.assertEqual(result.returncode, 0, result.stderr)
        tracked = self.git(vault, "ls-files").stdout.split()
        self.assertIn("new-note.md", tracked)
        self.assertEqual(self.git(vault, "status", "--porcelain").stdout, "")

    def test_non_repository_is_skipped_without_failing_the_job(self):
        plain = self.root / "not-a-repo"
        plain.mkdir()

        result = self.run_snapshot([plain])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("not a Git repository", result.stderr)


if __name__ == "__main__":
    unittest.main()
