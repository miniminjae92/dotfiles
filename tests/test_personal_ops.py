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

RECENT_CHECK = "2026-07-19T10:00:00+09:00"  # 고정 now(19일 21시) 기준 11시간 전


def observations(**overrides):
    base = {
        "listenerBaseline": [],
        "launchdBaseline": [],
        "softwareUpdateCheckedAt": RECENT_CHECK,
        "listenerCount": 0,
    }
    base.update(overrides)
    return base


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
            mock.patch.object(personal_ops, "emit_ops_event"),
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

    def collect_with(self, previous, listeners=({}, True), launchd=(), run_map=None):
        """설정 검사 4종을 전부 정상으로 두고 collect를 실행한다."""
        calls = []

        def fake_run(command, timeout=30):
            calls.append(command)
            binary = command[0]
            results = {
                "csrutil": (0, "System Integrity Protection status: enabled."),
                "spctl": (0, "assessments enabled"),
                "fdesetup": (0, "FileVault is On."),
                "socketfilterfw": (0, "Firewall is enabled. (State = 1)"),
                "softwareupdate": (0, "No new software available"),
                "tmutil": (0, "> Name : backup-disk"),
            }
            results.update(run_map or {})
            for key, result in results.items():
                if key in binary:
                    return result
            return 0, ""

        with mock.patch.object(personal_ops, "run", side_effect=fake_run), \
                mock.patch.object(personal_ops, "external_listeners", return_value=listeners), \
                mock.patch.object(personal_ops, "launchd_plists", return_value=set(launchd)), \
                mock.patch.object(personal_ops, "credential_paths", return_value=()):
            findings, obs = personal_ops.collect_security_findings(previous)
        return findings, obs, calls

    # --- security_command: 알림 라우팅 ---

    @mock.patch.object(personal_ops, "notify")
    @mock.patch.object(personal_ops, "collect_security_findings")
    def test_security_baseline_is_quiet(self, collect, notify):
        collect.return_value = ({}, observations(listenerBaseline=["node"]))

        self.assertEqual(personal_ops.security_command(), 0)

        notify.assert_not_called()
        state = json.loads(personal_ops.SECURITY_STATE.read_text(encoding="utf-8"))
        self.assertEqual(state["listenerBaseline"], ["node"])

    @mock.patch.object(personal_ops, "notify")
    @mock.patch.object(personal_ops, "collect_security_findings")
    def test_security_medium_change_writes_report_without_slack(self, collect, notify):
        item = personal_ops.finding("medium", "업데이트 있음", "macOS update")
        collect.return_value = ({"macos-updates": item}, observations())

        personal_ops.security_command()
        personal_ops.security_command()

        notify.assert_not_called()
        reports = list((self.report_root / "Security").glob("*.md"))
        self.assertEqual(len(reports), 1)

    @mock.patch.object(personal_ops, "notify")
    @mock.patch.object(personal_ops, "collect_security_findings")
    def test_security_high_finding_notifies_immediately(self, collect, notify):
        item = personal_ops.finding("high", "FileVault가 비활성 상태입니다", "Off")
        collect.return_value = ({"filevault-disabled": item}, observations())

        personal_ops.security_command()

        notify.assert_called_once()
        self.assertIn("high 포함", notify.call_args.args[3])

    @mock.patch.object(personal_ops, "notify")
    @mock.patch.object(personal_ops, "collect_security_findings")
    def test_security_resolved_only_is_report_only(self, collect, notify):
        item = personal_ops.finding("medium", "새 외부 TCP 리스너 프로세스가 감지되었습니다", "node")
        collect.return_value = ({"listener:node": item}, observations())
        personal_ops.security_command()

        collect.return_value = ({}, observations())
        personal_ops.security_command()

        notify.assert_not_called()
        reports = list((self.report_root / "Security").glob("*.md"))
        self.assertEqual(len(reports), 1)  # 고정 now → 같은 파일명에 덮어씀
        self.assertIn("listener:node", reports[0].read_text(encoding="utf-8"))

    # --- 리스너: 식별자·기준선 ---

    def test_listener_baseline_migrates_ports_and_drops_apple_daemons(self):
        baseline = personal_ops.normalized_listener_baseline(
            ["ControlCe:5000", "ControlCe:7000", "CrossEXSe:34581", "rapportd:60413", "node"]
        )

        self.assertEqual(baseline, {"CrossEXSe", "node"})

    def test_collect_flags_new_listener_process_with_ports(self):
        findings, obs, _ = self.collect_with(
            {"listenerBaseline": ["CrossEXSe:34581"], "softwareUpdateCheckedAt": RECENT_CHECK, "active": {}},
            listeners=({"node": {"4180", "3000"}, "CrossEXSe": {"34581"}}, True),
        )

        self.assertEqual([key for key in findings if key.startswith("listener:")], ["listener:node"])
        self.assertIn("3000, 4180", findings["listener:node"]["detail"])
        self.assertEqual(obs["listenerBaseline"], ["CrossEXSe"])
        self.assertEqual(obs["listenerCount"], 3)

    def test_collect_seeds_baselines_silently_on_first_run(self):
        findings, obs, _ = self.collect_with(
            {},
            listeners=({"node": {"3000"}}, True),
            launchd={"/Library/LaunchAgents/a.plist"},
        )

        self.assertFalse([key for key in findings if key.startswith(("listener:", "launchd:"))])
        self.assertEqual(obs["listenerBaseline"], ["node"])
        self.assertEqual(obs["launchdBaseline"], ["/Library/LaunchAgents/a.plist"])

    # --- launchd 퍼시스턴스 ---

    def test_collect_flags_new_launchd_registration(self):
        findings, _, _ = self.collect_with(
            {
                "listenerBaseline": ["node"],
                "launchdBaseline": ["/Library/LaunchAgents/a.plist"],
                "softwareUpdateCheckedAt": RECENT_CHECK,
                "active": {},
            },
            listeners=({"node": {"3000"}}, True),
            launchd={"/Library/LaunchAgents/a.plist", "/Library/LaunchAgents/b.plist"},
        )

        self.assertIn("launchd:/Library/LaunchAgents/b.plist", findings)

    # --- softwareupdate 주 1회 ---

    def test_software_update_carries_forward_between_weekly_checks(self):
        item = personal_ops.finding("medium", "권장 macOS 업데이트가 있습니다", "macOS Tahoe")
        findings, obs, calls = self.collect_with(
            {
                "listenerBaseline": ["node"],
                "softwareUpdateCheckedAt": RECENT_CHECK,
                "active": {"macos-updates": item},
            },
            listeners=({"node": {"3000"}}, True),
        )

        self.assertEqual(findings.get("macos-updates"), item)
        self.assertFalse(any("softwareupdate" in command[0] for command in calls))
        self.assertEqual(obs["softwareUpdateCheckedAt"], RECENT_CHECK)

    def test_software_update_runs_when_due(self):
        findings, obs, calls = self.collect_with(
            {
                "listenerBaseline": ["node"],
                "softwareUpdateCheckedAt": "2026-07-10T10:00:00+09:00",
                "active": {},
            },
            listeners=({"node": {"3000"}}, True),
            run_map={"softwareupdate": (0, "* Label: macOS Tahoe 26.6-25G72\n")},
        )

        self.assertTrue(any("softwareupdate" in command[0] for command in calls))
        self.assertIn("Tahoe", findings["macos-updates"]["detail"])
        self.assertEqual(obs["softwareUpdateCheckedAt"], personal_ops.now_local().isoformat())

    # --- 신규 체크: 백업·자격증명 ---

    def test_backup_missing_finding(self):
        findings, _, _ = self.collect_with(
            {"listenerBaseline": ["node"], "softwareUpdateCheckedAt": RECENT_CHECK, "active": {}},
            listeners=({}, True),
            run_map={"tmutil": (1, "tmutil: No destinations configured.")},
        )

        self.assertIn("backup-missing", findings)
        self.assertEqual(findings["backup-missing"]["severity"], "medium")

    def test_credential_findings_flags_loose_permissions_only(self):
        secret = Path(self.temporary_directory.name) / "auth.json"
        secret.write_text("{}", encoding="utf-8")
        secret.chmod(0o644)
        findings = {}
        with mock.patch.object(personal_ops, "credential_paths", return_value=(secret,)):
            personal_ops.credential_findings(findings)
        [(key, item)] = list(findings.items())
        self.assertTrue(key.startswith("cred-permissions:"))
        self.assertEqual(item["severity"], "high")

        secret.chmod(0o600)
        findings = {}
        with mock.patch.object(personal_ops, "credential_paths", return_value=(secret,)):
            personal_ops.credential_findings(findings)
        self.assertEqual(findings, {})

    # --- accept ---

    def test_accept_moves_findings_into_baselines(self):
        state = {
            "checkedAt": RECENT_CHECK,
            "active": {
                "listener:node": personal_ops.finding("medium", "리스너", "node"),
                "launchd:/Library/LaunchAgents/b.plist": personal_ops.finding(
                    "medium", "launchd", "b.plist"
                ),
                "backup-missing": personal_ops.finding("medium", "백업", "없음"),
            },
            "listenerBaseline": ["CrossEXSe"],
            "launchdBaseline": ["/Library/LaunchAgents/a.plist"],
        }
        personal_ops.SECURITY_STATE.parent.mkdir(parents=True, exist_ok=True)
        personal_ops.SECURITY_STATE.write_text(
            json.dumps(state, ensure_ascii=False), encoding="utf-8"
        )

        self.assertEqual(personal_ops.security_accept([]), 0)

        updated = json.loads(personal_ops.SECURITY_STATE.read_text(encoding="utf-8"))
        self.assertEqual(sorted(updated["active"]), ["backup-missing"])
        self.assertEqual(sorted(updated["listenerBaseline"]), ["CrossEXSe", "node"])
        self.assertEqual(
            sorted(updated["launchdBaseline"]),
            ["/Library/LaunchAgents/a.plist", "/Library/LaunchAgents/b.plist"],
        )

    # --- weekly (기존 유지) ---

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
