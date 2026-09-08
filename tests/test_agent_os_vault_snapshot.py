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
            self.git(vault, "push", "-q", "-u", "origin", "main")
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

    def run_check(self, vaults, extra_env=None):
        env = os.environ.copy()
        env.update(GIT_ENV)
        env["YGGDRASIL_VAULT"] = str(vaults[0])
        env["DEVELOPER_OS_VAULT"] = str(vaults[1] if len(vaults) > 1 else vaults[0])
        env["HOME"] = str(self.root / "home")
        env["PATH"] = f"/usr/bin:/bin:/usr/local/bin:{os.defpath}"
        env.update(extra_env or {})
        return subprocess.run(
            ["bash", str(SCRIPT), "--check"],
            text=True,
            capture_output=True,
            env=env,
            check=False,
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
        self.assertEqual(result.returncode, 1, result.stderr)
        # 무인 잡이 rebase 중간 상태를 남기면 다음 실행까지 연쇄로 깨진다.
        self.assertFalse((vault / ".git" / "rebase-merge").exists())
        self.assertFalse((vault / ".git" / "rebase-apply").exists())

    def test_conflict_still_attempts_the_other_vault_before_failing(self):
        remote = self.make_remote()
        conflicted = self.make_vault("conflicted", remote)
        other = self.make_vault("other")
        remote_writer = self.make_vault("remote-writer")
        self.git(remote_writer, "remote", "add", "origin", str(remote))
        self.git(remote_writer, "fetch", "-q", "origin", "main")
        self.git(remote_writer, "reset", "-q", "--hard", "origin/main")
        (remote_writer / "note.md").write_text("remote\n", encoding="utf-8")
        self.git(remote_writer, "commit", "-qam", "remote edit")
        self.git(remote_writer, "push", "-q", "origin", "main")
        (conflicted / "note.md").write_text("local\n", encoding="utf-8")
        (other / "later.md").write_text("must still commit\n", encoding="utf-8")

        result = self.run_snapshot([conflicted, other])

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("later.md", self.git(other, "ls-files").stdout.split())

    def test_snapshot_does_not_overwrite_fetch_head_used_by_another_fetcher(self):
        remote = self.make_remote()
        vault = self.make_vault("vault", remote)
        fetch_head = vault / ".git" / "FETCH_HEAD"
        fetch_head.write_text("unrelated fetch state\n", encoding="utf-8")

        result = self.run_snapshot([vault])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(fetch_head.read_text(encoding="utf-8"), "unrelated fetch state\n")

    def test_check_reports_local_tracking_divergence_without_changing_vault(self):
        remote = self.make_remote()
        vault = self.make_vault("vault", remote)
        other = self.make_vault("other")
        self.git(other, "remote", "add", "origin", str(remote))
        self.git(other, "fetch", "-q", "origin", "main")
        self.git(other, "reset", "-q", "--hard", "origin/main")
        (other / "remote.md").write_text("remote\n", encoding="utf-8")
        self.git(other, "add", "-A")
        self.git(other, "commit", "-q", "-m", "remote")
        self.git(other, "push", "-q", "origin", "main")
        # --check은 네트워크를 쓰지 않고 이미 갱신된 로컬 추적 참조만 비교한다.
        self.git(vault, "fetch", "-q", "origin", "main")
        (vault / "local.md").write_text("local\n", encoding="utf-8")
        self.git(vault, "add", "-A")
        self.git(vault, "commit", "-q", "-m", "local")
        before_head = self.git(vault, "rev-parse", "HEAD").stdout
        before_status = self.git(vault, "status", "--porcelain").stdout

        result = self.run_check([vault])

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("ahead=1 behind=1", result.stdout, (result.returncode, result.stderr))
        self.assertIn("local tracking refs only; remote freshness unverified", result.stdout)
        self.assertEqual(self.git(vault, "rev-parse", "HEAD").stdout, before_head)
        self.assertEqual(self.git(vault, "status", "--porcelain").stdout, before_status)

    def test_check_does_not_emit_an_ops_event_when_paths_fall_back(self):
        vault = self.make_vault("vault", self.make_remote())
        event_log = self.root / "ops-events.log"
        fake_bin = self.root / "bin"
        fake_bin.mkdir()
        fake_ops_event = fake_bin / "ops-event"
        fake_ops_event.write_text(
            "#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >> \"$OPS_EVENT_LOG\"\n",
            encoding="utf-8",
        )
        fake_ops_event.chmod(0o755)

        result = self.run_check(
            [vault],
            {
                "DOTFILES_DIR": str(self.root / "missing-dotfiles"),
                "OPS_EVENT_LOG": str(event_log),
                "PATH": f"{fake_bin}:/usr/bin:/bin",
            },
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(event_log.exists(), "--check must not record ops events")

    def test_snapshot_rebases_local_commit_onto_remote_advance_then_checks_clean(self):
        remote = self.make_remote()
        vault = self.make_vault("vault", remote)
        other = self.make_vault("other")
        self.git(other, "remote", "add", "origin", str(remote))
        self.git(other, "fetch", "-q", "origin", "main")
        self.git(other, "reset", "-q", "--hard", "origin/main")
        (other / "remote.md").write_text("from remote\n", encoding="utf-8")
        self.git(other, "add", "-A")
        self.git(other, "commit", "-q", "-m", "remote advance")
        self.git(other, "push", "-q", "origin", "main")
        (vault / "local.md").write_text("from local\n", encoding="utf-8")

        snapshot = self.run_snapshot([vault])
        checked = self.run_check([vault])

        self.assertEqual(snapshot.returncode, 0, snapshot.stderr)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertIn("ahead=0 behind=0", checked.stdout)
        self.assertTrue((vault / "remote.md").is_file())
        self.assertTrue((vault / "local.md").is_file())

    def test_check_fails_when_unsnapshotted_working_tree_changes_are_pending(self):
        remote = self.make_remote()
        vault = self.make_vault("vault", remote)
        (vault / "pending.md").write_text("not snapshot yet\n", encoding="utf-8")

        result = self.run_check([vault])

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("working tree changes pending", result.stderr)
        self.assertIn("pending.md", self.git(vault, "status", "--porcelain").stdout)

    def test_unreachable_remote_is_reported_as_offline_not_as_a_conflict(self):
        vault = self.make_vault("vault-offline")
        self.git(
            vault, "remote", "add", "origin", "git@127.0.0.1:1/nonexistent-vault.git"
        )

        result = self.run_snapshot([vault])

        self.assertNotIn("manual check needed", result.stderr)
        self.assertNotIn("manual merge needed", result.stderr)
        self.assertIn("offline/auth", result.stderr)

    def test_fetch_auth_failure_after_successful_ls_remote_is_best_effort(self):
        remote = self.make_remote()
        vault = self.make_vault("vault", remote)
        fake_bin = self.root / "bin"
        fake_bin.mkdir()
        fake_git = fake_bin / "git"
        fake_git.write_text(
            "#!/usr/bin/env bash\n"
            "for arg in \"$@\"; do\n"
            "  if [ \"$arg\" = fetch ]; then\n"
            "    printf 'fatal: Authentication failed\\n' >&2\n"
            "    exit 1\n"
            "  fi\n"
            "done\n"
            "exec /usr/bin/git \"$@\"\n",
            encoding="utf-8",
        )
        fake_git.chmod(0o755)

        result = self.run_snapshot([vault], {"PATH": f"{fake_bin}:/usr/bin:/bin"})

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("pull skipped (offline/auth)", result.stderr)
        self.assertNotIn("manual check needed", result.stderr)

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
