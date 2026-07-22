import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "personal-ops"
LOADER = importlib.machinery.SourceFileLoader("personal_ops", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
personal_ops = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(personal_ops)
KST = ZoneInfo("Asia/Seoul")


class PersonalOpsTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        root = Path(self.temporary_directory.name)
        self.state_root = root / "state"
        self.report_root = root / "reports"
        self.developer_vault = root / "mimir"
        self.patches = [
            mock.patch.object(personal_ops, "STATE_ROOT", self.state_root),
            mock.patch.object(personal_ops, "SECURITY_STATE", self.state_root / "security.json"),
            mock.patch.object(personal_ops, "REPORT_ROOT", self.report_root),
            mock.patch.object(personal_ops, "DEVELOPER_VAULT", self.developer_vault),
            mock.patch.object(
                personal_ops,
                "now_local",
                return_value=datetime(2026, 7, 19, 21, 0, tzinfo=KST),
            ),
        ]
        for patch in self.patches:
            patch.start()

    def tearDown(self):
        for patch in reversed(self.patches):
            patch.stop()
        self.temporary_directory.cleanup()

    @mock.patch.object(personal_ops, "notify")
    @mock.patch.object(personal_ops, "collect_security_findings", return_value=({}, {"rapportd:123"}))
    def test_security_baseline_is_quiet(self, _collect, notify):
        self.assertEqual(personal_ops.security_command(), 0)

        notify.assert_not_called()
        state = json.loads(personal_ops.SECURITY_STATE.read_text(encoding="utf-8"))
        self.assertEqual(state["listenerBaseline"], ["rapportd:123"])

    @mock.patch.object(personal_ops, "notify")
    @mock.patch.object(personal_ops, "collect_security_findings")
    def test_security_notifies_only_on_state_change(self, collect, notify):
        item = personal_ops.finding("medium", "업데이트 있음", "macOS update")
        collect.return_value = ({"macos-updates": item}, set())

        personal_ops.security_command()
        personal_ops.security_command()

        notify.assert_called_once()
        self.assertIn("새 이상 1건", notify.call_args.args[3])
        reports = list((self.report_root / "Security").glob("*.md"))
        self.assertEqual(len(reports), 1)

    @mock.patch.object(personal_ops, "notify")
    @mock.patch.object(personal_ops, "weekly_sources", return_value=("source", []))
    def test_weekly_no_agent_writes_once_and_links_report(self, _sources, notify):
        self.assertEqual(personal_ops.weekly_command(no_agent=True), 0)
        self.assertEqual(personal_ops.weekly_command(no_agent=True), 0)

        reports = list((self.report_root / "Weekly Reviews").glob("*.md"))
        self.assertEqual(len(reports), 1)
        self.assertIn("generator: rules", reports[0].read_text(encoding="utf-8"))
        notify.assert_called_once()
        self.assertIn("obsidian://open", notify.call_args.args[3])

    def test_friction_entries_filters_by_date_and_keeps_escalations(self):
        note = self.developer_vault / "00 Inbox" / "생산성 불편일기.md"
        note.parent.mkdir(parents=True, exist_ok=True)
        note.write_text(
            "## 미처리\n"
            "\n"
            "- [ ] 2026-07-18T10:00:00+09:00 | origin:agent | escalation: worker→planner | 마이그레이션 | 반복 실패\n"
            "- [ ] 2026-06-01T10:00:00+09:00 | origin:user | 오래된 항목\n"
            "- 타임스탬프 없는 줄\n",
            encoding="utf-8",
        )

        entries = personal_ops.friction_entries(datetime(2026, 7, 12, tzinfo=KST))

        self.assertEqual(len(entries), 1)
        self.assertIn("escalation: worker→planner", entries[0])

    def test_friction_entries_returns_empty_without_note(self):
        self.assertEqual(
            personal_ops.friction_entries(datetime(2026, 7, 12, tzinfo=KST)), []
        )

    def test_obsidian_link_uses_encoded_absolute_path(self):
        link = personal_ops.obsidian_link(Path("/tmp/My Report.md"), "열기")

        self.assertEqual(link, "<obsidian://open?path=%2Ftmp%2FMy%20Report.md|열기>")

    @mock.patch.object(personal_ops.subprocess, "run")
    @mock.patch.object(personal_ops, "codex_executable", return_value="/usr/local/bin/codex")
    def test_weekly_agent_is_ephemeral_read_only_and_low_reasoning(self, _codex, run):
        def execute(command, **_kwargs):
            output_path = Path(command[command.index("--output-last-message") + 1])
            output_path.write_text("## 완료한 일\n\n- 충분히 긴 주간 회고 결과입니다. " * 8)
            return mock.Mock(returncode=0)

        run.side_effect = execute

        result = personal_ops.generate_with_codex(
            "trusted source", datetime(2026, 7, 19, 21, 0, tzinfo=KST)
        )

        command = run.call_args.args[0]
        self.assertIsNotNone(result)
        self.assertIn("--ephemeral", command)
        self.assertIn("read-only", command)
        self.assertIn('model_reasoning_effort="low"', command)


if __name__ == "__main__":
    unittest.main()
