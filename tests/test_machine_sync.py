import base64
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "machine-sync"
LOADER = importlib.machinery.SourceFileLoader("machine_sync", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
machine_sync = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(machine_sync)


HOOKS = {
    "hooks": {
        "SessionStart": [{"hooks": [{"command": "start"}]}],
        "Stop": [{"hooks": [{"command": "capture"}, {"command": "notify"}]}],
    }
}


class MachineSyncTests(unittest.TestCase):
    def source_config(self):
        source_home = Path("/Users/miniminjae")
        state = {}
        for index, key in enumerate(machine_sync.expected_hook_keys(HOOKS, source_home)):
            state[key] = {"trusted_hash": f"sha256:{index:064x}"}
        return {"hooks": {"state": state}}, state

    def test_portable_hook_state_requires_every_handler_for_every_profile(self):
        config, expected = self.source_config()

        actual = machine_sync.portable_hook_state(
            config,
            HOOKS,
            Path("/Users/miniminjae"),
            Path("/Users/miniminjae"),
        )

        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 9)

    def test_portable_hook_state_rejects_untrusted_handler(self):
        config, _state = self.source_config()
        first_key = next(iter(config["hooks"]["state"]))
        del config["hooks"]["state"][first_key]["trusted_hash"]

        with self.assertRaises(machine_sync.SyncError):
            machine_sync.portable_hook_state(
                config,
                HOOKS,
                Path("/Users/miniminjae"),
                Path("/Users/miniminjae"),
            )

    def test_merge_codex_config_preserves_unmanaged_machine_state(self):
        _config, state = self.source_config()
        target = '''model = "gpt-test"
approval_policy = "never"

[projects."/tmp/local-only"]
trust_level = "trusted"

[hooks.state]

[hooks.state."/old/hooks.json:stop:0:0"]
trusted_hash = "sha256:old"

[shell_environment_policy.set]
LOCAL_ONLY = "preserved"
'''

        merged = machine_sync.merge_codex_config(
            target, machine_sync.EXPECTED_POLICY, state
        )

        self.assertIn('model = "gpt-test"', merged)
        self.assertIn('[projects."/tmp/local-only"]', merged)
        self.assertIn('LOCAL_ONLY = "preserved"', merged)
        self.assertNotIn('/old/hooks.json', merged)
        self.assertIn('approval_policy = "on-request"', merged)
        self.assertIn('sandbox_mode = "danger-full-access"', merged)

    def test_validate_source_rejects_failed_doctor(self):
        snapshot = {
            "status": "",
            "doctor_ok": False,
            "projects_ok": True,
            "policy": {},
            "hook_state": {},
            "hooks": "",
        }

        with self.assertRaisesRegex(machine_sync.SyncError, "정본 기기"):
            machine_sync.validate_source(snapshot)

    def test_validate_source_rejects_project_drift_unless_skipped(self):
        config, _state = self.source_config()
        snapshot = {
            "status": "",
            "doctor_ok": True,
            "projects_ok": False,
            "policy": machine_sync.EXPECTED_POLICY,
            "hook_state": config["hooks"]["state"],
            "hooks": base64.b64encode(json.dumps(HOOKS).encode()).decode(),
        }

        with self.assertRaisesRegex(machine_sync.SyncError, "프로젝트"):
            machine_sync.validate_source(snapshot)

        parsed, hooks, _raw = machine_sync.validate_source(
            snapshot, require_projects=False
        )
        self.assertEqual(parsed["approval_policy"], "on-request")
        self.assertEqual(hooks, HOOKS)

    def test_origin_contains_commit_requires_reachable_remote_ref(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            environment = {
                **os.environ,
                "GIT_AUTHOR_NAME": "Test",
                "GIT_AUTHOR_EMAIL": "test@example.com",
                "GIT_COMMITTER_NAME": "Test",
                "GIT_COMMITTER_EMAIL": "test@example.com",
            }
            tracked = root / "tracked.txt"
            tracked.write_text("published\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "tracked.txt"], check=True)
            subprocess.run(
                ["git", "-C", str(root), "commit", "-q", "-m", "published"],
                check=True,
                env=environment,
            )
            published = machine_sync.git_output(root, "rev-parse", "HEAD")
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "update-ref",
                    "refs/remotes/origin/main",
                    published,
                ],
                check=True,
            )
            tracked.write_text("local only\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "tracked.txt"], check=True)
            subprocess.run(
                ["git", "-C", str(root), "commit", "-q", "-m", "local only"],
                check=True,
                env=environment,
            )
            local_only = machine_sync.git_output(root, "rev-parse", "HEAD")

            self.assertTrue(machine_sync.origin_contains_commit(root, published))
            self.assertFalse(machine_sync.origin_contains_commit(root, local_only))

    def test_validate_account_links_rejects_non_shared_config(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            default = home / ".codex"
            account = home / ".codex-accounts" / "google"
            default.mkdir()
            account.mkdir(parents=True)
            (default / "config.toml").write_text("model = 'shared'\n", encoding="utf-8")
            (account / "config.toml").write_text("model = 'local'\n", encoding="utf-8")

            with self.assertRaisesRegex(machine_sync.SyncError, "공유 링크"):
                machine_sync.validate_account_links(home, allow_missing=True)

    def test_account_link_preflight_allows_missing_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            default = home / ".codex"
            default.mkdir()
            (default / "config.toml").write_text("model = 'shared'\n", encoding="utf-8")

            machine_sync.validate_account_links(home, allow_missing=True)


if __name__ == "__main__":
    unittest.main()
