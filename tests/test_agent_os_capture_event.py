import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "bin" / "agent-os-capture-event"
EVENT_SCHEMA = Path(__file__).parents[1] / "agent-os" / "schemas" / "event.schema.json"


class AgentOsCaptureEventTest(unittest.TestCase):
    def write_transcript(self, sessions, session_id, turn_id):
        sessions.mkdir(parents=True, exist_ok=True)
        transcript = sessions / f"rollout-{session_id}.jsonl"
        transcript.write_text(
            "\n".join(
                json.dumps(record)
                for record in [
                    {
                        "type": "turn_context",
                        "payload": {
                            "turn_id": turn_id,
                            "model": "gpt-5.6-sol",
                            "effort": "xhigh",
                        },
                    },
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "token_count",
                            "info": {
                                "total_token_usage": {
                                    "input_tokens": 100,
                                    "cached_input_tokens": 40,
                                    "output_tokens": 20,
                                    "reasoning_output_tokens": 10,
                                    "total_tokens": 120,
                                },
                                "last_token_usage": {
                                    "input_tokens": 8,
                                    "cached_input_tokens": 3,
                                    "output_tokens": 2,
                                    "reasoning_output_tokens": 1,
                                    "total_tokens": 10,
                                },
                                "model_context_window": 272000,
                            },
                        },
                    },
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        return transcript

    def run_capture(self, root, payload, extra_env=None):
        env = os.environ.copy()
        env["HOME"] = str(root / "home")
        env["AGENT_OS_STATE_DIR"] = str(root / "state")
        env.pop("AGENT_OS_SESSIONS_DIR", None)
        env.pop("CODEX_HOME", None)
        env.update(extra_env or {})
        result = subprocess.run(
            [str(SCRIPT)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

        event_files = list((root / "state" / "events").glob("*.jsonl"))
        self.assertEqual(len(event_files), 1)
        event = json.loads(event_files[0].read_text(encoding="utf-8"))
        schema = json.loads(EVENT_SCHEMA.read_text(encoding="utf-8"))
        self.assertLessEqual(set(event), set(schema["properties"]))
        return result, event

    def assert_complete_metrics(self, event):
        self.assertEqual(event["model"], "gpt-5.6-sol")
        self.assertEqual(event["reasoning_effort"], "xhigh")
        self.assertEqual(event["usage"]["session_total"]["total_tokens"], 120)
        self.assertEqual(event["usage"]["last_request"]["total_tokens"], 10)
        self.assertEqual(event["metrics_status"], "complete")

    def test_event_schema_declares_metrics_status_values(self):
        schema = json.loads(EVENT_SCHEMA.read_text(encoding="utf-8"))

        self.assertEqual(
            schema["properties"]["metrics_status"],
            {
                "type": "string",
                "enum": ["complete", "partial", "unavailable"],
            },
        )

    def test_codex_home_sessions_enrich_stop_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session_id = "019ff4e8-e3ae-7d61-8baf-fdcbd09e1c39"
            turn_id = "turn-account-home"
            transcript = self.write_transcript(
                root / "codex-home" / "sessions", session_id, turn_id
            )
            result, event = self.run_capture(
                root,
                {
                    "session_id": session_id,
                    "turn_id": turn_id,
                    "hook_event_name": "Stop",
                    "transcript_path": str(transcript),
                },
                {"CODEX_HOME": str(root / "codex-home")},
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_complete_metrics(event)

    def test_explicit_sessions_dir_wins_over_codex_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session_id = "session-explicit-root"
            turn_id = "turn-explicit-root"
            transcript = self.write_transcript(
                root / "explicit-sessions", session_id, turn_id
            )
            (root / "codex-home" / "sessions").mkdir(parents=True)
            result, event = self.run_capture(
                root,
                {
                    "session_id": session_id,
                    "turn_id": turn_id,
                    "hook_event_name": "Stop",
                    "transcript_path": str(transcript),
                },
                {
                    "AGENT_OS_SESSIONS_DIR": str(root / "explicit-sessions"),
                    "CODEX_HOME": str(root / "codex-home"),
                },
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_complete_metrics(event)

    def test_default_home_sessions_are_used_without_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session_id = "session-default-home"
            turn_id = "turn-default-home"
            transcript = self.write_transcript(
                root / "home" / ".codex" / "sessions", session_id, turn_id
            )
            result, event = self.run_capture(
                root,
                {
                    "session_id": session_id,
                    "turn_id": turn_id,
                    "hook_event_name": "Stop",
                    "transcript_path": str(transcript),
                },
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_complete_metrics(event)

    def test_model_only_stop_event_reports_partial_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result, event = self.run_capture(
                root,
                {
                    "session_id": "session-without-transcript",
                    "turn_id": "turn-without-transcript",
                    "hook_event_name": "Stop",
                    "model": "gpt-5.6-sol",
                    "transcript_path": None,
                },
                {"CODEX_HOME": str(root / "codex-home")},
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(event["model"], "gpt-5.6-sol")
            self.assertNotIn("reasoning_effort", event)
            self.assertNotIn("usage", event)
            self.assertEqual(event["metrics_status"], "partial")

    def test_transcript_outside_selected_root_reports_unavailable_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session_id = "session-outside-root"
            turn_id = "turn-outside-root"
            transcript = self.write_transcript(
                root / "outside-sessions", session_id, turn_id
            )
            (root / "codex-home" / "sessions").mkdir(parents=True)
            result, event = self.run_capture(
                root,
                {
                    "session_id": session_id,
                    "turn_id": turn_id,
                    "hook_event_name": "Stop",
                    "transcript_path": str(transcript),
                },
                {"CODEX_HOME": str(root / "codex-home")},
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIsNone(event["model"])
            self.assertNotIn("reasoning_effort", event)
            self.assertNotIn("usage", event)
            self.assertEqual(event["metrics_status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
