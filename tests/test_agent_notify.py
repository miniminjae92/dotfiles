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
    def test_generic_event_can_request_immediate_slack(self, _spawn_worker):
        result = agent_notify.main(
            [
                "event",
                "--source",
                "codex-usage",
                "--status",
                "attention",
                "--project",
                "google 90% used",
                "--local",
                "temporary",
                "--slack",
                "immediate",
                "--slack-destination",
                "usage",
            ],
            "",
        )

        self.assertEqual(result, 0)
        event = agent_notify.list_events()[0]
        self.assertEqual(event["local_delivery"], "temporary")
        self.assertEqual(event["slack_delivery"], "immediate")
        self.assertEqual(event["slack_destination"], "usage")
        self.assertTrue(event["slack_immediate"])

    @mock.patch.object(agent_notify, "post_slack")
    @mock.patch.object(
        agent_notify,
        "read_slack_webhook",
        return_value="https://hooks.slack.com/services/T/B/USAGE",
    )
    def test_usage_event_reads_usage_destination(self, read_webhook, post_slack):
        event = agent_notify.normalize_event(
            "codex-usage", "attention", {"cwd": "/tmp/sample"}
        )
        event.update(
            slack_destination="usage",
            slack_delivery="immediate",
            slack_immediate=True,
        )
        self.save_event(event)
        agent_notify.update_runtime_settings(slack_enabled=True)

        self.assertTrue(agent_notify.deliver_slack_event(event, datetime.now(timezone.utc)))

        read_webhook.assert_called_once_with("usage")
        post_slack.assert_called_once()

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
    def test_claude_hook_stores_only_metadata(self, _spawn_worker):
        payload = {
            "hook_event_name": "Stop",
            "cwd": "/Users/test/projects/sample",
            "session_id": "claude-session-1",
            "transcript_path": "/Users/test/.claude/projects/sample/transcript.jsonl",
        }

        result = agent_notify.main(["claude-hook"], json.dumps(payload))

        self.assertEqual(result, 0)
        event = agent_notify.list_events()[0]
        self.assertEqual(event["source"], "claude")
        self.assertEqual(event["status"], "complete")
        self.assertEqual(event["source_label"], "Claude")
        self.assertEqual(event["project"], "sample")
        self.assertEqual(event["session_id"], "claude-session-1")

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_claude_hook_notification_becomes_attention_event(self, _spawn_worker):
        payload = {
            "hook_event_name": "Notification",
            "cwd": "/Users/test/projects/sample",
            "session_id": "claude-session-2",
            "message": "Claude needs your permission to use Bash",
        }

        result = agent_notify.main(["claude-hook"], json.dumps(payload))

        self.assertEqual(result, 0)
        event = agent_notify.list_events()[0]
        self.assertEqual(event["status"], "attention")
        self.assertNotIn("permission to use Bash", json.dumps(event))

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_claude_hook_ignores_other_events(self, spawn_worker):
        payload = {"hook_event_name": "PreToolUse", "cwd": "/tmp/sample"}

        result = agent_notify.main(["claude-hook"], json.dumps(payload))

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

    @mock.patch.object(agent_notify, "send_osascript")
    @mock.patch.object(agent_notify, "alerter_path", return_value=None)
    def test_osascript_remains_fallback_when_alerter_is_missing(self, _alerter, send):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        self.save_event(event)

        agent_notify.run_worker(event["id"])

        send.assert_called_once()
        self.assertEqual(
            agent_notify.load_event(event["id"])["notification_backend"], "osascript"
        )

    @mock.patch.object(agent_notify, "run_alerter")
    @mock.patch.object(agent_notify, "send_osascript")
    @mock.patch.object(agent_notify, "alerter_path", return_value=None)
    @mock.patch.object(agent_notify, "local_notification_backend", return_value="osascript")
    def test_config_can_force_reliable_osascript_backend(
        self, _backend, _alerter, send, run_alerter
    ):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        self.save_event(event)

        self.assertEqual(agent_notify.run_worker(event["id"]), 0)

        send.assert_called_once()
        run_alerter.assert_not_called()
        self.assertEqual(
            agent_notify.load_event(event["id"])["notification_backend"], "osascript"
        )

    @mock.patch.object(agent_notify, "run_alerter", return_value="@TIMEOUT")
    @mock.patch.object(
        agent_notify, "alerter_path", return_value="/opt/homebrew/bin/alerter"
    )
    def test_temporary_notification_uses_alerter_timeout(self, _alerter, run_alerter):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        self.save_event(event)

        self.assertEqual(agent_notify.run_worker(event["id"]), 0)

        run_alerter.assert_called_once_with(event, "/opt/homebrew/bin/alerter")
        self.assertEqual(
            agent_notify.load_event(event["id"])["notification_backend"],
            "alerter",
        )
        self.assertTrue(agent_notify.is_pending(agent_notify.load_event(event["id"])))

    @mock.patch.object(agent_notify, "run_alerter", return_value="확인")
    @mock.patch.object(
        agent_notify, "alerter_path", return_value="/opt/homebrew/bin/alerter"
    )
    def test_persistent_notification_waits_for_and_handles_action(
        self, _alerter, run_alerter
    ):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        event["local_delivery"] = "persistent"
        self.save_event(event)

        self.assertEqual(agent_notify.run_worker(event["id"]), 0)

        run_alerter.assert_called_once_with(event, "/opt/homebrew/bin/alerter")
        self.assertIsNotNone(agent_notify.load_event(event["id"])["acknowledged_at"])

    @mock.patch.object(agent_notify, "send_osascript")
    @mock.patch.object(agent_notify, "run_alerter")
    def test_local_off_presents_nothing(self, run_alerter, send_osascript):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        event["local_delivery"] = "off"
        self.save_event(event)

        self.assertEqual(agent_notify.run_worker(event["id"]), 0)

        run_alerter.assert_not_called()
        send_osascript.assert_not_called()
        self.assertEqual(agent_notify.load_event(event["id"])["notification_backend"], "off")

    @mock.patch.object(agent_notify.subprocess, "run")
    def test_alerter_uses_actions_and_timeout(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="@TIMEOUT\n")
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})

        response = agent_notify.run_alerter(event, "/alerter")

        command = run.call_args.args[0]
        self.assertIn("--actions", command)
        self.assertIn("확인,터미널로 이동", command)
        self.assertNotIn("--sender", command)
        self.assertEqual(command[command.index("--timeout") + 1], "8")
        self.assertEqual(response, "@TIMEOUT")

    @mock.patch.object(agent_notify, "acknowledge_event")
    @mock.patch.object(agent_notify, "open_event_target")
    def test_alerter_content_click_focuses_target_and_acknowledges(
        self, open_target, acknowledge
    ):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})

        agent_notify.handle_alerter_response(event, "@CONTENTCLICKED")

        open_target.assert_called_once_with(event)
        acknowledge.assert_called_once_with(event["id"], opened=True)

    @mock.patch.object(agent_notify, "spawn_worker")
    @mock.patch.object(
        agent_notify, "alerter_path", return_value="/opt/homebrew/bin/alerter"
    )
    def test_local_test_uses_persistent_clickable_policy(self, _alerter, _spawn_worker):
        self.assertEqual(agent_notify.main(["test"], ""), 0)

        event = agent_notify.list_events()[0]
        self.assertEqual(event["policy_name"], "test")
        self.assertEqual(event["local_delivery"], "persistent")
        self.assertEqual(event["slack_delivery"], "off")

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

    @mock.patch.object(agent_notify, "post_slack")
    @mock.patch.object(
        agent_notify,
        "read_slack_webhook",
        return_value="https://hooks.slack.com/services/T/B/X",
    )
    def test_slack_off_policy_never_escalates(self, _read_webhook, post_slack):
        current_time = datetime(2026, 7, 16, 7, 0, tzinfo=timezone.utc)
        event = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/sample"}
        )
        event["created_at"] = (current_time - timedelta(hours=1)).isoformat()
        event["slack_delivery"] = "off"
        self.save_event(event)
        agent_notify.update_runtime_settings(slack_enabled=True)

        self.assertEqual(agent_notify.sweep(current_time), 0)
        post_slack.assert_not_called()

    @mock.patch.object(
        agent_notify,
        "read_slack_webhook",
        return_value="https://hooks.slack.com/services/T/B/X",
    )
    @mock.patch.object(agent_notify, "spawn_worker")
    def test_away_once_marks_only_next_event_for_immediate_slack(
        self, _spawn_worker, _read_webhook
    ):
        agent_notify.update_runtime_settings(slack_enabled=True)

        self.assertEqual(agent_notify.main(["away", "once"], ""), 0)
        first = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/first"}
        )
        second = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/second"}
        )
        agent_notify.enqueue_event(first)
        agent_notify.enqueue_event(second)

        self.assertTrue(agent_notify.load_event(first["id"])["slack_immediate"])
        self.assertEqual(agent_notify.load_event(first["id"])["local_delivery"], "off")
        self.assertFalse(agent_notify.load_event(second["id"])["slack_immediate"])
        self.assertEqual(agent_notify.load_event(second["id"])["slack_delivery"], "delayed")
        self.assertIsNone(agent_notify.runtime_settings().get("next_policy"))

    @mock.patch.object(
        agent_notify,
        "read_slack_webhook",
        return_value="https://hooks.slack.com/services/T/B/X",
    )
    @mock.patch.object(agent_notify, "spawn_worker")
    def test_timed_away_mode_persists_until_expiration(self, _spawn_worker, _read_webhook):
        agent_notify.update_runtime_settings(slack_enabled=True)

        self.assertEqual(agent_notify.main(["away", "on", "--for", "2h"], ""), 0)
        first = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/first"}
        )
        second = agent_notify.normalize_event(
            "future-agent", "error", {"cwd": "/tmp/second"}
        )
        agent_notify.enqueue_event(first)
        agent_notify.enqueue_event(second)

        self.assertTrue(agent_notify.load_event(first["id"])["slack_immediate"])
        self.assertTrue(agent_notify.load_event(second["id"])["slack_immediate"])
        self.assertEqual(agent_notify.runtime_settings()["active_policy"]["name"], "away")
        self.assertIsNotNone(agent_notify.runtime_settings()["active_policy"]["until"])

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_expired_away_mode_returns_to_delayed_delivery(self, _spawn_worker):
        agent_notify.update_runtime_settings(
            slack_enabled=True,
            active_policy={
                "name": "away",
                "local": "off",
                "slack": "immediate",
                "until": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
            },
        )
        event = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/sample"}
        )

        agent_notify.enqueue_event(event)

        self.assertFalse(agent_notify.load_event(event["id"])["slack_immediate"])
        self.assertEqual(agent_notify.load_event(event["id"])["policy_name"], "normal")
        self.assertEqual(agent_notify.runtime_settings()["active_policy"]["name"], "normal")

    @mock.patch.object(agent_notify, "read_slack_webhook", return_value=None)
    def test_away_mode_requires_configured_slack(self, _read_webhook):
        agent_notify.update_runtime_settings(slack_enabled=True)

        self.assertEqual(agent_notify.main(["away", "once"], ""), 1)
        self.assertIsNone(agent_notify.runtime_settings().get("next_policy"))

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_quiet_mode_disables_both_delivery_channels(self, _spawn_worker):
        self.assertEqual(agent_notify.main(["mode", "quiet"], ""), 0)
        event = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/sample"}
        )

        agent_notify.enqueue_event(event)

        saved = agent_notify.load_event(event["id"])
        self.assertEqual(saved["local_delivery"], "off")
        self.assertEqual(saved["slack_delivery"], "off")

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_custom_mode_supports_independent_delivery_combination(self, _spawn_worker):
        self.assertEqual(
            agent_notify.main(
                ["mode", "set", "--local", "persistent", "--slack", "off"], ""
            ),
            0,
        )
        event = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/sample"}
        )

        agent_notify.enqueue_event(event)

        saved = agent_notify.load_event(event["id"])
        self.assertEqual(saved["policy_name"], "custom")
        self.assertEqual(saved["local_delivery"], "persistent")
        self.assertEqual(saved["slack_delivery"], "off")

    def test_help_documents_mode_set_values_and_direct_examples(self):
        for arguments in (["--help"], ["mode", "--help"]):
            stdout = io.StringIO()
            with mock.patch("sys.stdout", stdout):
                self.assertEqual(agent_notify.main(arguments, ""), 0)
            help_text = stdout.getvalue()
            self.assertIn("--local <off|temporary|persistent>", help_text)
            self.assertIn("--slack <off|delayed|immediate>", help_text)
            self.assertIn("mode set --local persistent --slack off", help_text)
            self.assertIn("mode set --local temporary --slack off", help_text)
            self.assertIn("mode set --local persistent --slack immediate", help_text)
            self.assertIn("mode set --local off --slack immediate", help_text)

    @mock.patch.object(agent_notify, "post_slack")
    @mock.patch.object(
        agent_notify,
        "read_slack_webhook",
        return_value="https://hooks.slack.com/services/T/B/X",
    )
    @mock.patch.object(agent_notify, "send_osascript")
    @mock.patch.object(agent_notify.shutil, "which", return_value=None)
    def test_worker_sends_away_event_to_slack_immediately(
        self, _which, _send_osascript, _read_webhook, post_slack
    ):
        agent_notify.update_runtime_settings(slack_enabled=True)
        event = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/sample"}
        )
        event["slack_immediate"] = True
        event["slack_delivery"] = "immediate"
        self.save_event(event)

        self.assertEqual(agent_notify.run_worker(event["id"]), 0)

        post_slack.assert_called_once()
        self.assertIsNotNone(agent_notify.load_event(event["id"])["escalated_at"])

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

    @mock.patch.object(agent_notify, "tmux_executable", return_value="/opt/homebrew/bin/tmux")
    @mock.patch.object(agent_notify.subprocess, "run")
    def test_open_focuses_recorded_tmux_client_window_and_pane(self, run, _tmux):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        event.update(
            tmux_target="work:2.1",
            tmux_session="work",
            terminal_app="iTerm2",
            terminal_bundle_id="com.googlecode.iterm2",
        )

        def result(command, **_kwargs):
            if "list-clients" in command:
                return subprocess.CompletedProcess(command, 0, stdout="/dev/ttys001\twork\n")
            return subprocess.CompletedProcess(command, 0, stdout="")

        run.side_effect = result

        agent_notify.open_event_target(event)

        commands = [call.args[0] for call in run.call_args_list]
        self.assertIn(
            ["/opt/homebrew/bin/tmux", "switch-client", "-c", "/dev/ttys001", "-t", "work"],
            commands,
        )
        self.assertIn(
            ["/opt/homebrew/bin/tmux", "select-pane", "-t", "work:2.1"],
            commands,
        )
        self.assertIn(["/usr/bin/open", "-b", "com.googlecode.iterm2"], commands)

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
