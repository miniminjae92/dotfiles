import importlib.machinery
import importlib.util
import os
import tempfile
import unittest
import json
from pathlib import Path


ASX = Path(__file__).parents[1] / "bin" / "asx"


def load_asx():
    loader = importlib.machinery.SourceFileLoader("asx_test_module", str(ASX))
    spec = importlib.util.spec_from_loader("asx_test_module", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class AsxSessionRootsTest(unittest.TestCase):
    def test_default_and_account_isolated_codex_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            default = Path(tmp) / ".codex"
            accounts = Path(tmp) / ".codex-accounts"
            expected = [
                default / "sessions",
                default / "archived_sessions",
                accounts / "google" / "sessions",
                accounts / "naver" / "archived_sessions",
            ]
            for root in expected:
                root.mkdir(parents=True)

            old_default = os.environ.get("ASX_CODEX_HOME")
            old_accounts = os.environ.get("ASX_CODEX_ACCOUNTS_HOME")
            os.environ["ASX_CODEX_HOME"] = str(default)
            os.environ["ASX_CODEX_ACCOUNTS_HOME"] = str(accounts)
            try:
                module = load_asx()
                self.assertEqual(
                    module.codex_session_roots(),
                    [os.path.realpath(p) for p in expected],
                )
            finally:
                if old_default is None:
                    os.environ.pop("ASX_CODEX_HOME", None)
                else:
                    os.environ["ASX_CODEX_HOME"] = old_default
                if old_accounts is None:
                    os.environ.pop("ASX_CODEX_ACCOUNTS_HOME", None)
                else:
                    os.environ["ASX_CODEX_ACCOUNTS_HOME"] = old_accounts

    def test_codex_injected_agents_message_is_not_a_user_turn(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "rollout-test.jsonl"
            rows = [
                {
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"text": "# AGENTS.md instructions\n\n<INSTRUCTIONS>x</INSTRUCTIONS>"}],
                    }
                },
                {
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"text": "실제 질문"}],
                    }
                },
            ]
            log.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            module = load_asx()
            record = module.parse(str(log), "codex")
            self.assertEqual(record["msgs"], [("user", "실제 질문")])


if __name__ == "__main__":
    unittest.main()
