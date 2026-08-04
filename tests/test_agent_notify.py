import importlib.machinery
import importlib.util
import io
import json
import os
import signal
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
                "AGENT_NOTIFY_POLICY": "",
                "TMUX_PANE": "",
                # sweep 테스트가 실제 이벤트 스트림을 오염시키지 않게 격리
                "OPS_STATE_DIR": str(root / "ops"),
            },
        )
        self.environment.start()

    def tearDown(self):
        self.environment.stop()
        self.temporary_directory.cleanup()

    def save_event(self, event):
        agent_notify.atomic_write_json(agent_notify.event_path(event["id"]), event)

    def fake_alerter_process(self, pid=4242, stdout="", returncode=0):
        process = mock.Mock()
        process.pid = pid
        process.returncode = returncode
        process.communicate.return_value = (stdout, "")
        return process

    def owned_alerter_event(self, pid=9001, path="/opt/homebrew/bin/alerter", cwd="/tmp/owned"):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": cwd})
        event["alerter_pid"] = pid
        event["alerter_path"] = path
        self.save_event(event)
        return event

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

    @mock.patch.object(agent_notify, "post_slack")
    @mock.patch.object(agent_notify, "read_slack_webhook")
    def test_destination_disabled_does_not_deliver_or_read_webhook(self, read_webhook, post_slack):
        event = agent_notify.normalize_event(
            "codex-usage", "attention", {"cwd": "/tmp/sample"}
        )
        event.update(slack_destination="usage", slack_delivery="immediate")
        self.save_event(event)
        agent_notify.update_runtime_settings(
            slack_enabled=True,
            slack_destinations={"agent": True, "usage": False},
        )

        self.assertFalse(agent_notify.deliver_slack_event(event, datetime.now(timezone.utc)))
        read_webhook.assert_not_called()
        post_slack.assert_not_called()

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
    def test_codex_permission_request_becomes_priority_attention(self, _spawn_worker):
        payload = {
            "hook_event_name": "PermissionRequest",
            "cwd": "/Users/test/projects/sample",
            "session_id": "codex-session-1",
            "turn_id": "turn-1",
            "tool_name": "Bash",
            "tool_input": {"command": "secret command"},
        }

        result = agent_notify.main(["codex-hook"], json.dumps(payload))

        self.assertEqual(result, 0)
        event = agent_notify.list_events()[0]
        self.assertEqual(event["source"], "codex")
        self.assertEqual(event["status"], "attention")
        self.assertEqual(event["kind"], "permission_request")
        self.assertEqual(event["source_label"], "Codex 승인 대기")
        self.assertNotIn("secret command", json.dumps(event))

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_codex_hook_ignores_other_event(self, spawn_worker):
        payload = {"hook_event_name": "PreToolUse", "cwd": "/tmp/sample"}

        result = agent_notify.main(["codex-hook"], json.dumps(payload))

        self.assertEqual(result, 0)
        self.assertEqual(agent_notify.list_events(), [])
        spawn_worker.assert_not_called()

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_duplicate_hook_delivery_for_same_turn_enqueues_once(self, spawn_worker):
        payload = {
            "hook_event_name": "Stop",
            "cwd": "/Users/test/projects/sample",
            "session_id": "codex-session-1",
            "turn_id": "turn-1",
        }

        agent_notify.main(["codex-hook"], json.dumps(payload))
        agent_notify.main(["codex-hook"], json.dumps(payload))

        self.assertEqual(len(agent_notify.list_events()), 1)
        spawn_worker.assert_called_once()

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
    def test_claude_hook_precompact_becomes_labeled_attention(self, _spawn_worker):
        payload = {
            "hook_event_name": "PreCompact",
            "cwd": "/Users/test/projects/sample",
            "session_id": "claude-session-3",
            "trigger": "auto",
        }

        result = agent_notify.main(["claude-hook"], json.dumps(payload))

        self.assertEqual(result, 0)
        event = agent_notify.list_events()[0]
        self.assertEqual(event["status"], "attention")
        self.assertEqual(event["source_label"], "Claude 컨텍스트")

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

    @mock.patch.object(agent_notify.subprocess, "Popen")
    def test_alerter_uses_actions_and_timeout(self, popen):
        popen.return_value = self.fake_alerter_process(stdout="@TIMEOUT\n")
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        self.save_event(event)

        response = agent_notify.run_alerter(event, "/alerter")

        command = popen.call_args.args[0]
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
    def test_environment_policy_scopes_quiet_to_process_tree(self, _spawn_worker):
        payload = {
            "hook_event_name": "Stop",
            "cwd": "/tmp/bulk",
            "session_id": "bulk-session-1",
        }

        with mock.patch.dict(os.environ, {"AGENT_NOTIFY_POLICY": "quiet"}):
            self.assertEqual(agent_notify.main(["claude-hook"], json.dumps(payload)), 0)

        event = agent_notify.list_events()[0]
        self.assertEqual(event["policy_name"], "env:quiet")
        self.assertEqual(event["local_delivery"], "off")
        self.assertEqual(event["slack_delivery"], "off")
        self.assertEqual(agent_notify.active_policy(agent_notify.runtime_settings())["name"], "normal")

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_unknown_environment_policy_falls_back_to_global_mode(self, _spawn_worker):
        event = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/sample"}
        )
        stderr = io.StringIO()

        with mock.patch.dict(os.environ, {"AGENT_NOTIFY_POLICY": "loud"}):
            with mock.patch("sys.stderr", stderr):
                agent_notify.enqueue_event(event)

        saved = agent_notify.load_event(event["id"])
        self.assertEqual(saved["policy_name"], "normal")
        self.assertIn("loud", stderr.getvalue())

    @mock.patch.object(agent_notify, "spawn_worker")
    def test_explicit_event_policy_beats_environment_policy(self, _spawn_worker):
        with mock.patch.dict(os.environ, {"AGENT_NOTIFY_POLICY": "quiet"}):
            result = agent_notify.main(
                [
                    "event",
                    "--source",
                    "future-agent",
                    "--project",
                    "sample",
                    "--local",
                    "persistent",
                    "--slack",
                    "off",
                ],
                "",
            )

        self.assertEqual(result, 0)
        event = agent_notify.list_events()[0]
        self.assertEqual(event["local_delivery"], "persistent")
        self.assertEqual(event["slack_delivery"], "off")

    @mock.patch.object(
        agent_notify,
        "read_slack_webhook",
        return_value="https://hooks.slack.com/services/T/B/X",
    )
    @mock.patch.object(agent_notify, "spawn_worker")
    def test_environment_policy_preserves_one_shot_next_policy(
        self, _spawn_worker, _read_webhook
    ):
        agent_notify.update_runtime_settings(slack_enabled=True)
        self.assertEqual(agent_notify.main(["away", "once"], ""), 0)
        bulk = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/bulk"}
        )
        interactive = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/interactive"}
        )

        with mock.patch.dict(os.environ, {"AGENT_NOTIFY_POLICY": "quiet"}):
            agent_notify.enqueue_event(bulk)
        agent_notify.enqueue_event(interactive)

        self.assertEqual(agent_notify.load_event(bulk["id"])["policy_name"], "env:quiet")
        self.assertTrue(agent_notify.load_event(interactive["id"])["slack_immediate"])
        self.assertIsNone(agent_notify.runtime_settings().get("next_policy"))

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
        self.assertTrue(agent_notify.slack_enabled("agent"))
        self.assertFalse(agent_notify.slack_enabled("usage"))

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

    # --- alerter 소유권과 회수 ------------------------------------------------

    @mock.patch.object(agent_notify.subprocess, "Popen")
    def test_persistent_notification_is_bounded(self, popen):
        process = self.fake_alerter_process(stdout="확인\n")
        popen.return_value = process
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        event["local_delivery"] = "persistent"
        self.save_event(event)

        agent_notify.run_alerter(event, "/alerter")

        command = popen.call_args.args[0]
        self.assertEqual(command[command.index("--timeout") + 1], "1800")
        self.assertEqual(process.communicate.call_args.kwargs["timeout"], 1810)

    @mock.patch.object(agent_notify.subprocess, "Popen")
    def test_alerter_ownership_recorded_while_waiting_then_released(self, popen):
        process = self.fake_alerter_process(pid=4242)
        popen.return_value = process
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        self.save_event(event)
        observed = []

        def observe(timeout=None):
            observed.append(agent_notify.load_event(event["id"])["alerter_pid"])
            return ("확인\n", "")

        process.communicate.side_effect = observe

        agent_notify.run_alerter(event, "/alerter")

        # 대기하는 동안에는 디스크에 소유권이 남아 있어야 회수가 가능하다.
        self.assertEqual(observed, [4242])
        self.assertIsNone(agent_notify.load_event(event["id"])["alerter_pid"])

    @mock.patch.object(agent_notify.os, "kill")
    @mock.patch.object(agent_notify, "process_table")
    def test_reaper_ignores_alerter_it_does_not_own(self, process_table, kill):
        # 다른 도구가 띄운 동명 프로세스. 상한을 한참 넘겼지만 우리 것이 아니다.
        process_table.return_value = {
            9001: (99999, 900 * 1024, "/opt/other-tool/alerter")
        }
        self.save_event(
            agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        )

        self.assertEqual(agent_notify.reap_runaway_alerters(), 0)
        kill.assert_not_called()

    @mock.patch.object(agent_notify.os, "kill")
    @mock.patch.object(agent_notify, "process_table")
    def test_reaper_kills_owned_alerter_past_lifetime_limit(self, process_table, kill):
        process_table.return_value = {
            9001: (
                agent_notify.ALERTER_MAX_LIFETIME_SECONDS + 1,
                1024,
                "/opt/homebrew/bin/alerter",
            )
        }
        event = self.owned_alerter_event()

        self.assertEqual(agent_notify.reap_runaway_alerters(), 1)
        kill.assert_called_once_with(9001, signal.SIGKILL)
        self.assertIsNone(agent_notify.load_event(event["id"])["alerter_pid"])

    @mock.patch.object(agent_notify.os, "kill")
    @mock.patch.object(agent_notify, "process_table")
    def test_reaper_kills_owned_alerter_past_memory_limit(self, process_table, kill):
        process_table.return_value = {
            9001: (10, agent_notify.ALERTER_MAX_RSS_KB + 1, "/opt/homebrew/bin/alerter")
        }
        self.owned_alerter_event()

        self.assertEqual(agent_notify.reap_runaway_alerters(), 1)
        kill.assert_called_once_with(9001, signal.SIGKILL)

    @mock.patch.object(agent_notify.os, "kill")
    @mock.patch.object(agent_notify, "process_table")
    def test_reaper_skips_recycled_pid(self, process_table, kill):
        # PID가 재사용돼 전혀 다른 실행 파일을 돌리고 있다.
        process_table.return_value = {9001: (99999, 900 * 1024, "/usr/bin/python3")}
        event = self.owned_alerter_event()

        self.assertEqual(agent_notify.reap_runaway_alerters(), 0)
        kill.assert_not_called()
        self.assertIsNone(agent_notify.load_event(event["id"])["alerter_pid"])

    @mock.patch.object(agent_notify.os, "kill")
    @mock.patch.object(agent_notify, "process_table")
    def test_reaper_leaves_alerter_under_limits(self, process_table, kill):
        process_table.return_value = {
            9001: (60, 10 * 1024, "/opt/homebrew/bin/alerter")
        }
        event = self.owned_alerter_event()

        self.assertEqual(agent_notify.reap_runaway_alerters(), 0)
        kill.assert_not_called()
        self.assertEqual(agent_notify.load_event(event["id"])["alerter_pid"], 9001)

    # --- pending 적재 방지 ----------------------------------------------------

    @mock.patch.object(agent_notify, "alerter_path", return_value=None)
    @mock.patch.object(agent_notify, "send_osascript")
    def test_local_off_and_slack_off_is_acknowledged_immediately(self, _osascript, _alerter):
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        event["local_delivery"] = "off"
        event["slack_delivery"] = "off"
        self.save_event(event)

        agent_notify.run_worker(event["id"])

        self.assertIsNotNone(agent_notify.load_event(event["id"])["acknowledged_at"])

    def test_local_off_with_slack_delayed_stays_pending(self):
        # Slack 지연 에스컬레이션 기회를 뺏으면 안 된다.
        event = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/sample"})
        event["local_delivery"] = "off"
        event["slack_delivery"] = "delayed"
        event["slack_immediate"] = False
        self.save_event(event)

        agent_notify.run_worker(event["id"])

        self.assertIsNone(agent_notify.load_event(event["id"])["acknowledged_at"])

    def test_sweep_expires_pending_past_ttl(self):
        current_time = datetime(2026, 7, 26, 7, 0, tzinfo=timezone.utc)
        stale = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/stale"})
        stale["created_at"] = (current_time - timedelta(days=4)).isoformat()
        fresh = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/fresh"})
        fresh["created_at"] = (current_time - timedelta(days=1)).isoformat()
        self.save_event(stale)
        self.save_event(fresh)

        agent_notify.sweep(current_time)

        self.assertIsNotNone(agent_notify.load_event(stale["id"])["acknowledged_at"])
        self.assertIsNone(agent_notify.load_event(fresh["id"])["acknowledged_at"])

    def test_sweep_prunes_resolved_events_past_retention(self):
        current_time = datetime(2026, 7, 26, 7, 0, tzinfo=timezone.utc)
        old_resolved = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/old"})
        old_resolved["created_at"] = (current_time - timedelta(days=40)).isoformat()
        old_resolved["acknowledged_at"] = (current_time - timedelta(days=39)).isoformat()
        fresh_resolved = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/new"})
        fresh_resolved["acknowledged_at"] = (current_time - timedelta(days=5)).isoformat()
        old_pending = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/wait"})
        old_pending["created_at"] = (current_time - timedelta(days=40)).isoformat()
        for event in (old_resolved, fresh_resolved, old_pending):
            self.save_event(event)

        agent_notify.sweep(current_time)

        self.assertFalse(agent_notify.event_path(old_resolved["id"]).exists())
        self.assertTrue(agent_notify.event_path(fresh_resolved["id"]).exists())
        # 오래된 pending은 TTL로 '지금' 확정될 뿐 파일은 보존기간을 새로 산다
        self.assertTrue(agent_notify.event_path(old_pending["id"]).exists())

    def test_write_pending_summary_projects_pending_count(self):
        pending = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/a"})
        acknowledged = agent_notify.normalize_event("future-agent", "complete", {"cwd": "/tmp/b"})
        acknowledged["acknowledged_at"] = agent_notify.isoformat()
        self.save_event(pending)
        self.save_event(acknowledged)

        self.assertEqual(agent_notify.write_pending_summary(), 1)

        summary = json.loads(agent_notify.pending_summary_path().read_text())
        self.assertEqual(summary["count"], 1)
        self.assertEqual(summary["oldest_created_at"], pending["created_at"])

    def test_status_json_prioritizes_permission_requests_and_includes_mode(self):
        complete = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/complete"}
        )
        permission = agent_notify.normalize_event(
            "codex", "attention", {"cwd": "/tmp/approval"}
        )
        permission["kind"] = "permission_request"
        self.save_event(complete)
        self.save_event(permission)
        output = io.StringIO()

        with mock.patch("sys.stdout", output):
            self.assertEqual(agent_notify.main(["status", "--json"], ""), 0)

        result = json.loads(output.getvalue())
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(result["counts"]["pending"], 2)
        self.assertEqual(result["counts"]["permission_requests"], 1)
        self.assertEqual(result["counts"]["attention"], 0)
        self.assertEqual(result["events"][0]["kind"], "permission_request")
        self.assertEqual(result["mode"]["local"], "temporary")
        self.assertEqual(result["mode"]["slack"], "delayed")

    # --- 일괄 ack ------------------------------------------------------------

    @mock.patch.object(agent_notify, "remove_notification")
    def test_bulk_ack_never_calls_alerter_remove(self, remove_notification):
        # alerter --remove는 건당 타임아웃까지 블로킹된다. 일괄 처리에서 쓰면 끝나지 않는다.
        for index in range(3):
            self.save_event(
                agent_notify.normalize_event(
                    "future-agent", "complete", {"cwd": f"/tmp/bulk-{index}"}
                )
            )

        self.assertEqual(agent_notify.ack_command("--all"), 0)

        remove_notification.assert_not_called()

    @mock.patch.object(agent_notify, "remove_notification")
    def test_ack_completed_all_keeps_attention_pending(self, remove_notification):
        complete = agent_notify.normalize_event(
            "future-agent", "complete", {"cwd": "/tmp/complete"}
        )
        attention = agent_notify.normalize_event(
            "future-agent", "attention", {"cwd": "/tmp/attention"}
        )
        self.save_event(complete)
        self.save_event(attention)

        self.assertEqual(agent_notify.ack_command("--completed"), 0)

        self.assertIsNotNone(agent_notify.load_event(complete["id"])["acknowledged_at"])
        self.assertIsNone(agent_notify.load_event(attention["id"])["acknowledged_at"])
        remove_notification.assert_not_called()

    @mock.patch.object(agent_notify.os, "kill")
    @mock.patch.object(agent_notify, "process_table")
    @mock.patch.object(agent_notify, "remove_notification")
    def test_bulk_ack_terminates_owned_alerter(self, remove_notification, process_table, kill):
        process_table.return_value = {
            9001: (30, 1024, "/opt/homebrew/bin/alerter")
        }
        event = self.owned_alerter_event()

        self.assertEqual(agent_notify.ack_command("--all"), 0)

        kill.assert_called_once_with(9001, signal.SIGKILL)
        remove_notification.assert_not_called()
        self.assertIsNotNone(agent_notify.load_event(event["id"])["acknowledged_at"])


if __name__ == "__main__":
    unittest.main()
