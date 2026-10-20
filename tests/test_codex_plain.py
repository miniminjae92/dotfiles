import importlib.machinery
import importlib.util
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "bin/codex-plain"
LOADER = importlib.machinery.SourceFileLoader("codex_plain", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
plain = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(plain)


class CodexPlainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.home = self.base / "personal"
        self.project = self.base / "project with spaces"
        self.project.mkdir()
        (self.project / "AGENTS.md").write_text("project instructions stay")
        self.state = self.home / ".local/state/codex-plain"
        self.account = self.home / ".codex-accounts/naver"
        self.account.mkdir(parents=True)
        (self.account / "auth.json").write_text("fixture auth must never be copied or read")
        self.source_config = ('model="fixture-model"\nmodel_reasoning_effort="low"\nservice_tier="fast"\n'
                              'notify=["personal-hook"]\ninstructions="personal instructions"\n'
                              '[features]\nplugins=true\nmemories=true\n'
                              '[tui]\nstatus_line=["model-name"]\n'
                              f'[projects.{json.dumps(str(self.project))}]\ntrust_level="trusted"\n')
        (self.account / "config.toml").write_text(self.source_config)
        for path in (".agents/skills/personal", ".codex/skills/personal", ".agents/skills/group/nested"):
            skill = self.home / path
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: fixture-personal\ndescription: MUST NOT BE IMPORTED\n---\nfixture content")
        (self.home / ".codex/AGENTS.md").write_text("personal instructions")
        (self.home / ".codex/hooks.json").write_text("personal hook")
        self.fakebin = self.base / "fakebin"
        self.fakebin.mkdir()
        self.capture = self.base / "capture.json"
        executable = self.fakebin / "codex"
        executable.write_text('#!' + sys.executable + '\nimport json, os, pathlib, sys\n'
                              'pathlib.Path(os.environ["PLAIN_CAPTURE"]).write_text(json.dumps({"argv":sys.argv[1:], "env":dict(os.environ)}))\n'
                              'sys.exit(int(os.environ.get("PLAIN_EXIT", "0")))\n')
        executable.chmod(0o755)
        self.env = dict(os.environ, HOME=str(self.home), PATH=str(self.fakebin) + os.pathsep + os.environ["PATH"],
                        PLAIN_CAPTURE=str(self.capture), AGENT_MASTER_TASK_ID="stale", AGENT_MASTER_STATE_DIR="ignored",
                        CODEX_HOME="ignored", CODEX_SESSION_ID="stale", CODEX_THREAD_ID="stale",
                        OPENAI_API_KEY="fixture", CODEX_API_KEY="fixture", OPENAI_BASE_URL="http://invalid.fixture",
                        OPENAI_ORG_ID="fixture-org", OPENAI_PROJECT_ID="fixture-project")

    def cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=self.project,
                                env=self.env, text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def start(self, *args):
        self.cli("--account", "naver", "--goal", "fixture goal", *args)
        captured = json.loads(self.capture.read_text())
        home = Path(captured["env"]["CODEX_HOME"])
        row = json.loads((home / plain.MANIFEST).read_text())
        return home, row, captured

    def test_new_session_is_independent_and_preserves_project(self):
        home, row, captured = self.start()
        self.assertTrue(home.is_relative_to(self.state))
        self.assertEqual((home / "auth.json").resolve(), self.account / "auth.json")
        self.assertTrue((home / "auth.json").is_symlink())
        self.assertEqual((self.account / "config.toml").read_text(), self.source_config)
        config = plain.config_values(home / "config.toml")
        self.assertEqual(config["model"], "fixture-model")
        self.assertEqual(config["model_reasoning_effort"], "low")
        self.assertEqual(config["service_tier"], "fast")
        self.assertEqual(config["tui"]["status_line"], ["model-name"])
        self.assertEqual(config["projects"][str(self.project)]["trust_level"], "trusted")
        self.assertNotIn("notify", config)
        self.assertNotIn("instructions", config)
        self.assertNotIn("features", config)
        for name in ("AGENTS.md", "hooks.json", "agents", "skills", "memories", "plugins"):
            self.assertFalse((home / name).exists())
        self.assertEqual((self.project / "AGENTS.md").read_text(), "project instructions stay")
        argv = captured["argv"]
        self.assertEqual(argv[:3], ["--no-daemon", "-C", str(self.project)])
        self.assertIn('features.memories=false', argv)
        self.assertIn('features.plugins=false', argv)
        self.assertIn('features.apps=false', argv)
        skill_arg = next(arg for arg in argv if arg.startswith("skills.config="))
        self.assertIn(str(self.home / ".agents/skills/personal/SKILL.md"), skill_arg)
        self.assertIn("enabled=false", skill_arg)
        self.assertNotIn("AGENT_MASTER_TASK_ID", captured["env"])
        self.assertNotIn("AGENT_MASTER_STATE_DIR", captured["env"])
        for key in ("CODEX_SESSION_ID", "CODEX_THREAD_ID", "OPENAI_API_KEY", "CODEX_API_KEY",
                    "OPENAI_BASE_URL", "OPENAI_ORG_ID", "OPENAI_PROJECT_ID"):
            self.assertNotIn(key, captured["env"])
        self.assertFalse((self.home / ".local/state/agent-master").exists())
        self.assertEqual(len(row["id"]), 12)

    def test_dry_run_and_lists_do_not_create_files_or_execute(self):
        result = self.cli("--account", "naver", "--dry-run")
        self.assertEqual(json.loads(result.stdout)["account"], "naver")
        self.assertFalse(self.state.exists())
        self.assertFalse(self.capture.exists())
        self.assertEqual(json.loads(self.cli("resume", "--all", "--json").stdout), [])
        self.assertFalse(self.state.exists())

    def test_resume_same_home_and_sanitizes_config(self):
        home, row, _ = self.start()
        sessions = home / "sessions/2026/10"
        sessions.mkdir(parents=True)
        thread_id = '11111111-1111-4111-8111-111111111111'
        (sessions / "fixture.jsonl").write_text(json.dumps({'type': 'session_meta', 'payload': {'id': thread_id, 'source': 'cli', 'cwd': str(self.project)}}) + '\n')
        config = home / "config.toml"
        config.write_text(config.read_text().replace('fixture-model', 'changed-model') + '\n[mcp_servers.personal]\ncommand="personal-plugin"\n')
        self.cli("resume", row["id"])
        captured = json.loads(self.capture.read_text())
        self.assertEqual(captured["env"]["CODEX_HOME"], str(home))
        self.assertEqual(captured["argv"][-2:], ["resume", thread_id])
        self.assertEqual(json.loads((home / plain.MANIFEST).read_text())["thread_id"], thread_id)
        self.assertEqual(plain.config_values(config)["model"], "changed-model")
        self.assertNotIn("mcp_servers", plain.config_values(config))
        self.assertEqual(len(list(self.state.glob("homes/*/*/plain-session.json"))), 1)

    def test_resume_without_transcript_restarts_goal(self):
        home, row, _ = self.start()
        self.cli("resume", row["id"])
        self.assertEqual(json.loads(self.capture.read_text())["argv"][-1], "fixture goal")

    def test_resume_filters_and_last(self):
        home, first, _ = self.start()
        other = self.base / "other project"
        other.mkdir()
        self.cli("--cwd", str(other), "--account", "naver")
        local = json.loads(self.cli("resume", "--json").stdout)
        all_rows = json.loads(self.cli("resume", "--all", "--json").stdout)
        self.assertEqual([r["id"] for r in local], [first["id"]])
        self.assertEqual(len(all_rows), 2)
        self.cli("resume", "--last")
        self.assertEqual(json.loads(self.capture.read_text())["env"]["CODEX_HOME"], str(home))
        self.assertIn(first["id"], self.cli("resume", "--list").stdout)
        self.cli("resume", first["id"], "--account", "google", expected=2)
        self.cli("resume", first["id"], "--last", expected=2)
        self.cli("resume", "../../escape", expected=2)

    def test_two_accounts_require_selection_then_use_last_account(self):
        google = self.home / ".codex-accounts/google"
        google.mkdir()
        (google / "auth.json").write_text("fixture")
        self.cli(expected=2)
        self.start()
        self.cli()
        self.assertIn("naver", json.loads(self.capture.read_text())["env"]["CODEX_HOME"])
        self.cli("--account", "google")
        captured = json.loads(self.capture.read_text())
        self.assertIn("google", captured["env"]["CODEX_HOME"])
        self.assertTrue((Path(captured["env"]["CODEX_HOME"]) / "auth.json").is_symlink())

    def test_reject_injected_instructions_and_auth_retarget(self):
        home, row, _ = self.start()
        (home / "AGENTS.md").write_text("injected")
        self.cli("resume", row["id"], expected=2)
        (home / "AGENTS.md").unlink()
        (home / "auth.json").unlink()
        (home / "auth.json").symlink_to(self.project / "AGENTS.md")
        self.cli("resume", row["id"], expected=2)

    def test_child_exit_code_is_preserved_and_session_remains_resumable(self):
        self.env["PLAIN_EXIT"] = "7"
        self.cli("--account", "naver", expected=7)
        self.assertEqual(len(json.loads(self.cli("resume", "--json").stdout)), 1)

    def test_explicit_state_dir_has_no_am_dependency(self):
        isolated = self.base / "independent-state"
        result = self.cli("--state-dir", str(isolated), "--account", "naver", "--dry-run")
        self.assertTrue(Path(json.loads(result.stdout)["home"]).is_relative_to(isolated))
        self.assertFalse(isolated.exists())

    def test_state_environment_default_and_cli_override(self):
        custom = self.base / "env-state"
        self.env["CODEX_PLAIN_STATE_DIR"] = str(custom)
        result = self.cli("--account", "naver", "--dry-run")
        self.assertTrue(Path(json.loads(result.stdout)["home"]).is_relative_to(custom))
        explicit = self.base / "flag-state"
        result = self.cli("--state-dir", str(explicit), "--account", "naver", "--dry-run")
        self.assertTrue(Path(json.loads(result.stdout)["home"]).is_relative_to(explicit))
        self.assertFalse(custom.exists())
        self.assertFalse(explicit.exists())

    def rollout(self, home, directory, identity, source="cli", **meta):
        folder = home / directory
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / (identity + ".jsonl")
        path.write_text(json.dumps({"type": "session_meta", "payload": dict(id=identity, source=source, **meta)}) + "\n")
        return path

    def test_resume_binds_archived_parent_ignores_child_and_cwd(self):
        home, row, _ = self.start()
        parent = "11111111-1111-4111-8111-111111111111"
        child = "22222222-2222-4222-8222-222222222222"
        self.rollout(home, "archived_sessions", parent, cwd="/changed/cwd")
        self.rollout(home, "sessions", child, source={"subagent": {"thread_spawn": {"parent_thread_id": parent}}})
        self.cli("resume", row["id"])
        self.assertEqual(json.loads(self.capture.read_text())["argv"][-2:], ["resume", parent])
        self.rollout(home, "sessions", "33333333-3333-4333-8333-333333333333")
        self.cli("resume", row["id"])
        self.assertEqual(json.loads(self.capture.read_text())["argv"][-2:], ["resume", parent])

    def test_resume_ambiguous_or_malformed_rollouts_fail_without_launch(self):
        home, row, _ = self.start()
        self.rollout(home, "sessions", "11111111-1111-4111-8111-111111111111")
        self.rollout(home, "sessions", "22222222-2222-4222-8222-222222222222")
        self.capture.unlink()
        self.cli("resume", row["id"], expected=2)
        self.assertFalse(self.capture.exists())
        for path in (home / "sessions").glob("*.jsonl"):
            path.write_text("malformed fixture\n")
        self.cli("resume", row["id"], expected=2)
        self.assertFalse(self.capture.exists())

    @unittest.skipUnless(os.environ.get("CODEX_PLAIN_NATIVE_PROBE"), "optional installed CLI probe")
    def test_installed_cli_features_and_prompt_isolation(self):
        executable = shutil.which("codex")
        self.assertIsNotNone(executable)
        clean = self.base / "native-clean"
        clean.mkdir()
        (clean / "config.toml").write_text(plain.clean_config(plain.config_values(self.account / "config.toml"), self.project))
        env = {k: v for k, v in self.env.items() if not k.startswith("AGENT_MASTER_") and k not in
               ("OPENAI_API_KEY", "CODEX_API_KEY", "CODEX_SESSION_ID", "CODEX_THREAD_ID",
                "OPENAI_BASE_URL", "OPENAI_ORG_ID", "OPENAI_PROJECT_ID")}
        env["CODEX_HOME"] = str(clean)
        with patch.dict(os.environ, env, clear=True):
            flags = list(plain.ISOLATION)
            flags.append("skills.config=[" + ",".join("{path=" + json.dumps(p) + ",enabled=false}" for p in plain.personal_skills()) + "]")
        options = [arg for value in flags for arg in ("--config", value)]
        help_result = subprocess.run([executable, "--help"], cwd=self.project, env=env, capture_output=True, text=True, timeout=20)
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("--no-daemon", help_result.stdout)
        features = subprocess.run([executable, *options, "features", "list"], cwd=self.project,
                                  env=env, capture_output=True, text=True, timeout=20)
        self.assertEqual(features.returncode, 0, features.stderr)
        feature_values = {line.split()[0]: line.split()[-1] for line in features.stdout.splitlines() if line.split()}
        for feature in ("memories", "remote_plugin", "plugins", "apps"):
            self.assertEqual(feature_values[feature], "false")
        prompt = subprocess.run([executable, *options, "debug", "prompt-input", "fixture input"], cwd=self.project,
                                env=env, capture_output=True, text=True, timeout=20)
        self.assertEqual(prompt.returncode, 0, prompt.stderr)
        self.assertIn("project instructions stay", prompt.stdout)
        self.assertNotIn("personal instructions", prompt.stdout)
        self.assertNotIn("MUST NOT BE IMPORTED", prompt.stdout)
        self.assertNotIn("group/nested", prompt.stdout)

    def test_clean_config_does_not_read_auth_or_personal_skills(self):
        with patch.dict(os.environ, self.env, clear=True), patch.object(Path, "read_text", side_effect=AssertionError("must not read")):
            paths = plain.personal_skills()
            self.assertEqual(len(paths), 3)
            session = {"account": "naver", "id": "abcdef123456", "cwd": str(self.project), "goal": ""}
            self.assertIn("--no-daemon", plain.plan(self.state, session, False)["argv"])


if __name__ == "__main__":
    unittest.main()
