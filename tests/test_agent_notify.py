import importlib.machinery
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "agent-notify"
LOADER = importlib.machinery.SourceFileLoader("agent_notify", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
agent_notify = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(agent_notify)


class AgentNotifyTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        root = Path(self.temporary_directory.name)
        self.environment = mock.patch.dict(
            os.environ,
            {
                "AGENT_NOTIFY_STATE_DIR": str(root / "state"),
                "AGENT_NOTIFY_CONFIG": str(root / "missing-config.json"),
                "TMUX_PANE": "",
            },
        )
        self.environment.start()

    def tearDown(self):
        self.environment.stop()
        self.temporary_directory.cleanup()

    def save_event(self, event):
        agent_notify.atomic_write_json(agent_notify.event_path(event["id"]), event)

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_generic_source_uses_provider_neutral_schema(self, spawn_worker):
        result = agent_notify.main(
            [
                "event",
                "--source",
                "future-agent",
                "--label",
                "Future Agent",
                "--status",
                "attention",
                "--project",
                "sample",
                "--session",
                "session-1",
            ],
            "",
        )

        self.assertEqual(result, 0)
        event = agent_notify.list_events()[0]
        self.assertEqual(event["source"], "future-agent")
        self.assertEqual(event["source_label"], "Future Agent")
        self.assertEqual(event["status"], "attention")
        self.assertNotIn("model", event)
        spawn_worker.assert_called_once_with(event["id"])

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_codex_stores_only_metadata(self, _spawn_worker):
        payload = {
            "type": "agent-turn-complete",
            "cwd": "/Users/test/projects/sample",
            "thread-id": "thread-1",
            "input-messages": ["secret prompt"],
            "last-assistant-message": "secret answer",
        }

        result = agent_notify.main(["codex", json.dumps(payload)], "")

        self.assertEqual(result, 0)
        serialized = json.dumps(agent_notify.list_events()[0], ensure_ascii=False)
        self.assertIn("sample", serialized)
        self.assertNotIn("secret prompt", serialized)
        self.assertNotIn("secret answer", serialized)

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_codex_hook_ignores_non_stop_event(self, spawn_worker):
        payload = {"hook_event_name": "PreToolUse", "cwd": "/tmp/sample"}

        result = agent_notify.main(["codex-hook"], json.dumps(payload))

        self.assertEqual(result, 0)
        self.assertEqual(agent_notify.list_events(), [])
        spawn_worker.assert_not_called()

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_agy_error_enqueues_event_and_allows_stop(self, _spawn_worker):
        payload = {
            "terminationReason": "error",
            "error": "sensitive failure details",
            "workspacePaths": ["/Users/test/projects/sample"],
            "conversationId": "conversation-1",
        }
        stdout = io.StringIO()

        with mock.patch("sys.stdout", stdout):
            result = agent_notify.main(["agy"], json.dumps(payload))

        self.assertEqual(result, 0)
        event = agent_notify.list_events()[0]
        self.assertEqual(event["status"], "error")
        self.assertNotIn("sensitive failure details", json.dumps(event))
        self.assertEqual(stdout.getvalue(), '{"decision":"allow"}\n')

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_new_event_supersedes_pending_event_from_same_session(self, _spawn_worker):
        first = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/sample", "session_id": "same"}
        )
        second = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/sample", "session_id": "same"}
        )

        agent_notify.enqueue_event(first)
        agent_notify.enqueue_event(second)

        self.assertIsNotNone(agent_notify.load_event(first["id"])["superseded_at"])
        self.assertTrue(agent_notify.is_pending(agent_notify.load_event(second["id"])))

    @mock.patch.object(agent_notify, "run_alerter", return_value="확인")
    @mock.patch.object(agent_notify.shutil, "which", return_value="/opt/homebrew/bin/alerter")
    def test_alerter_acknowledges_event(self, _which, _run_alerter):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        self.save_event(event)

        result = agent_notify.run_worker(event["id"])

        self.assertEqual(result, 0)
        self.assertIsNotNone(agent_notify.load_event(event["id"])["acknowledged_at"])

    @mock.patch.object(agent_notify, "run_alerter", return_value="@CLOSED")
    @mock.patch.object(agent_notify.shutil, "which", return_value="/opt/homebrew/bin/alerter")
    def test_closing_as_later_keeps_event_pending(self, _which, _run_alerter):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        self.save_event(event)

        agent_notify.run_worker(event["id"])

        self.assertTrue(agent_notify.is_pending(agent_notify.load_event(event["id"])))

    @mock.patch.object(agent_notify, "send_osascript")
    @mock.patch.object(agent_notify.shutil, "which", return_value=None)
    def test_osascript_remains_fallback_when_alerter_is_missing(self, _which, send):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        self.save_event(event)

        agent_notify.run_worker(event["id"])

        send.assert_called_once()
        self.assertEqual(
            agent_notify.load_event(event["id"])["notification_backend"], "osascript"
        )

    @mock.patch.object(agent_notify, "post_slack")
    @mock.patch.object(agent_notify, "read_slack_webhook", return_value="https://hooks.slack.com/services/T/B/X")
    def test_sweep_escalates_only_due_pending_event(self, _read_webhook, post_slack):
        current_time = datetime(2026, 7, 16, 7, 0, tzinfo=timezone.utc)
        due = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/due"})
        due["created_at"] = (current_time - timedelta(minutes=11)).isoformat()
        future = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/future"})
        future["created_at"] = (current_time - timedelta(minutes=1)).isoformat()
        self.save_event(due)
        self.save_event(future)
        agent_notify.update_runtime_settings(slack_enabled=True)

        result = agent_notify.sweep(current_time)

        self.assertEqual(result, 0)
        post_slack.assert_called_once()
        self.assertIsNotNone(agent_notify.load_event(due["id"])["escalated_at"])
        self.assertIsNone(agent_notify.load_event(future["id"])["escalated_at"])

    @mock.patch.object(agent_notify, "read_slack_webhook")
    def test_disabled_slack_does_not_read_keychain(self, read_webhook):
        self.assertEqual(agent_notify.sweep(), 0)
        read_webhook.assert_not_called()

    @mock.patch.object(agent_notify, "read_slack_webhook", return_value="https://hooks.slack.com/services/T/B/X")
    @mock.patch.object(agent_notify.subprocess, "run")
    def test_slack_configure_uses_interactive_keychain_prompt(self, run, _read_webhook):
        run.return_value = subprocess.CompletedProcess([], 0)

        result = agent_notify.configure_slack()

        self.assertEqual(result, 0)
        command = run.call_args.args[0]
        self.assertEqual(command[-1], "-w")
        self.assertNotIn("https://hooks.slack.com", " ".join(command))
        self.assertTrue(agent_notify.slack_enabled())

    @mock.patch.object(agent_notify.subprocess, "run")
    def test_local_timeout_is_used_only_after_slack_is_enabled(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="@TIMEOUT", stderr="")
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})

        agent_notify.run_alerter(event, "/alerter")
        self.assertNotIn("--timeout", run.call_args.args[0])

        agent_notify.update_runtime_settings(slack_enabled=True)
        agent_notify.run_alerter(event, "/alerter")
        command = run.call_args.args[0]
        self.assertIn("--timeout", command)
        self.assertEqual(command[command.index("--timeout") + 1], "600")

    @mock.patch.object(agent_notify, "remove_notification")
    def test_ack_removes_persistent_notification(self, remove_notification):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        self.save_event(event)

        result = agent_notify.ack_command(event["id"][:8])

        self.assertEqual(result, 0)
        remove_notification.assert_called_once()
        self.assertIsNotNone(agent_notify.load_event(event["id"])["acknowledged_at"])


if __name__ == "__main__":
    unittest.main()
