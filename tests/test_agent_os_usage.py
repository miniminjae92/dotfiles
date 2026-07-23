import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "bin" / "agent-os-usage"


def event(session_id, recorded_at, total):
    return {
        "session_id": session_id,
        "recorded_at": recorded_at,
        "usage": {
            "session_total": {
                "input_tokens": total,
                "cached_input_tokens": 0,
                "output_tokens": 1,
                "reasoning_output_tokens": 0,
                "total_tokens": total + 1,
            }
        },
    }


class AgentOsUsageTest(unittest.TestCase):
    def run_usage(self, *args, extra_env=None):
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events"
            events.mkdir()
            rows = [
                event("old-session", "2026-07-20T00:00:00Z", 10),
                event("current-session", "2026-07-21T00:00:00Z", 20),
            ]
            (events / "events.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["AGENT_OS_STATE_DIR"] = tmp
            env.pop("CODEX_THREAD_ID", None)
            env.pop("CLAUDECODE", None)
            env.update(extra_env or {})
            return subprocess.run(
                [str(SCRIPT), *args],
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )

    def test_current_codex_thread_is_selected(self):
        result = self.run_usage(extra_env={"CODEX_THREAD_ID": "current-session"})
        self.assertEqual(result.returncode, 0)
        self.assertIn("session: current-session", result.stdout)

    def test_unknown_current_thread_does_not_fallback(self):
        result = self.run_usage(extra_env={"CODEX_THREAD_ID": "missing"})
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("session: current-session", result.stdout)

    def test_claude_context_refuses_codex_fallback(self):
        result = self.run_usage(extra_env={"CLAUDECODE": "1"})
        self.assertEqual(result.returncode, 2)
        self.assertIn("refusing Codex fallback", result.stderr)

    def test_latest_requires_explicit_flag(self):
        result = self.run_usage("--latest")
        self.assertEqual(result.returncode, 0)
        self.assertIn("session: current-session", result.stdout)


if __name__ == "__main__":
    unittest.main()
