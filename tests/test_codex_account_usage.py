import importlib.machinery
import importlib.util
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "codex-account-usage"
LOADER = importlib.machinery.SourceFileLoader("codex_account_usage", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
codex_account_usage = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(codex_account_usage)
KST = ZoneInfo("Asia/Seoul")


def snapshot(used: int, resets_at: int = 1784888313):
    return {
        "rateLimits": {
            "primary": {
                "usedPercent": used,
                "windowDurationMins": 10080,
                "resetsAt": resets_at,
            },
            "planType": "team",
        },
        "rateLimitResetCredits": {"availableCount": 0, "credits": []},
    }


class CodexAccountUsageTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.environment = mock.patch.dict(
            os.environ,
            {"CODEX_USAGE_STATE": str(Path(self.temporary_directory.name) / "state.json")},
        )
        self.environment.start()

    def tearDown(self):
        self.environment.stop()
        self.temporary_directory.cleanup()

    def test_summary_reports_used_remaining_and_reset(self):
        message = codex_account_usage.summary("google", snapshot(16))

        self.assertIn("사용 16%", message)
        self.assertIn("잔여 84%", message)
        self.assertIn("7일 창", message)
        self.assertIn("reset credit 0", message)

    @mock.patch.object(codex_account_usage, "notify")
    @mock.patch.object(codex_account_usage, "query")
    def test_monitor_sends_threshold_and_daily_reports(self, query, notify):
        query.side_effect = [snapshot(90), snapshot(20)]

        result = codex_account_usage.run_monitor(datetime(2026, 7, 17, 9, 5, tzinfo=KST))

        self.assertEqual(result, 0)
        messages = [call.args[0] for call in notify.call_args_list]
        self.assertIn("google: 주간 한도 90% 사용 · 10% 남음", messages)
        self.assertTrue(any(message.startswith("google: 사용 90%") for message in messages))
        self.assertTrue(any(message.startswith("naver: 사용 20%") for message in messages))

    @mock.patch.object(codex_account_usage, "notify")
    @mock.patch.object(codex_account_usage, "query")
    def test_monitor_detects_large_usage_drop_as_reset(self, query, notify):
        codex_account_usage.write_state(
            {
                "lastDailyReport": "2026-07-17",
                "profiles": {
                    "google": {"usedPercent": 94, "resetsAt": 1784872347},
                    "naver": {"usedPercent": 10, "resetsAt": 1784872347},
                },
            }
        )
        query.side_effect = [snapshot(4), snapshot(11)]

        codex_account_usage.run_monitor(datetime(2026, 7, 17, 21, 0, tzinfo=KST))

        messages = [call.args[0] for call in notify.call_args_list]
        self.assertEqual(messages, ["google: 사용량 94% → 4%, 한도 갱신 감지"])

    @mock.patch.object(codex_account_usage, "notify")
    @mock.patch.object(codex_account_usage, "query")
    def test_logged_out_profiles_do_not_send_notifications(self, query, notify):
        query.side_effect = codex_account_usage.UsageError("Not logged in")

        result = codex_account_usage.run_monitor(datetime(2026, 7, 17, 10, 0, tzinfo=KST))

        self.assertEqual(result, 0)
        notify.assert_not_called()

    @mock.patch.object(codex_account_usage, "notify")
    @mock.patch.object(codex_account_usage, "query")
    def test_monitor_falls_back_to_existing_default_login(self, query, notify):
        query.side_effect = [
            codex_account_usage.UsageError("Not logged in"),
            codex_account_usage.UsageError("Not logged in"),
            snapshot(16),
        ]

        codex_account_usage.run_monitor(datetime(2026, 7, 17, 9, 5, tzinfo=KST))

        messages = [call.args[0] for call in notify.call_args_list]
        self.assertEqual(len(messages), 1)
        self.assertTrue(messages[0].startswith("default: 사용 16%"))


if __name__ == "__main__":
    unittest.main()
