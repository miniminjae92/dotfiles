import datetime
import importlib.machinery
import importlib.util
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "ops-digest"
LOADER = importlib.machinery.SourceFileLoader("ops_digest", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
ops_digest = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(ops_digest)


def event(source, kind, severity="info", ts="2026-08-04T10:00:00+09:00", **payload):
    return {
        "schema_version": 1,
        "ts": ts,
        "source": source,
        "kind": kind,
        "severity": severity,
        **payload,
    }


class OpsDigestTest(unittest.TestCase):
    def test_event_message_prefers_message_key(self):
        ev = event("x", "error", message="boom", detail="무시됨")

        self.assertEqual(ops_digest.event_message(ev), "boom")

    def test_event_message_falls_back_to_payload_pairs(self):
        ev = event("personal-ops-security", "finding", "medium", active=11, new=1)

        self.assertEqual(ops_digest.event_message(ev), "active=11 new=1")

    def test_render_groups_repeated_errors_with_count(self):
        now = datetime.datetime.fromisoformat("2026-08-04T21:00:00+09:00")
        events = [
            event(
                "codex-account-usage",
                "error",
                "high",
                ts=f"2026-08-04T0{index}:00:00+09:00",
                message="default: 응답 시간 초과",
            )
            for index in range(3)
        ]

        markdown = ops_digest.render_markdown(ops_digest.build_digest(events, 7, now))

        self.assertIn("오류 3건", markdown)
        self.assertIn("×3", markdown)
        self.assertEqual(markdown.count("default: 응답 시간 초과"), 1)

    def test_render_surfaces_medium_findings_with_message(self):
        now = datetime.datetime.fromisoformat("2026-08-04T21:00:00+09:00")
        events = [
            event(
                "session-harvest",
                "error",
                "medium",
                message="codex 마이닝 실패 — 스텁 적재",
            ),
            event(
                "codex-account-usage",
                "finding",
                "medium",
                message="프로파일 조회 실패 1건 — default: 시간 초과",
            ),
        ]

        markdown = ops_digest.render_markdown(ops_digest.build_digest(events, 7, now))

        self.assertIn("codex 마이닝 실패", markdown)
        self.assertIn("[medium] `codex-account-usage`", markdown)

    @mock.patch.object(ops_digest.platform, "node", return_value="minjae-iMac.local")
    def test_resolve_out_path_expands_host_token(self, _node):
        resolved = ops_digest.resolve_out_path("~/vault/다이제스트 {host}.md")

        self.assertTrue(resolved.endswith("/vault/다이제스트 minjae-iMac.md"))

    @mock.patch.object(ops_digest.subprocess, "run")
    def test_notify_skips_when_no_signal(self, run):
        digest = {"errors": [], "findings_attention": [], "sources_silent": []}

        ops_digest.notify_digest(digest, None)

        run.assert_not_called()

    def test_snapshot_freshness_quiet_when_recent_push(self):
        now = datetime.datetime.fromisoformat("2026-08-06T21:00:00+09:00")
        events = [
            event("vault-snapshot", "run", ts="2026-08-06T20:00:00+09:00",
                  committed=1, pushed=2, push_failed=0, conflicted=0),
        ]

        self.assertEqual(ops_digest.snapshot_freshness(events, now), [])

    def test_snapshot_freshness_alerts_on_24h_silence(self):
        now = datetime.datetime.fromisoformat("2026-08-06T21:00:00+09:00")
        events = [
            event("vault-snapshot", "run", ts="2026-08-04T10:00:00+09:00",
                  committed=1, pushed=1, push_failed=0, conflicted=0),
        ]

        alerts = ops_digest.snapshot_freshness(events, now)

        self.assertEqual(len(alerts), 1)
        self.assertIn("침묵 24h+", alerts[0])

    def test_snapshot_freshness_alerts_on_committed_without_push(self):
        now = datetime.datetime.fromisoformat("2026-08-06T21:00:00+09:00")
        events = [
            event("vault-snapshot", "run", ts="2026-08-06T19:00:00+09:00",
                  committed=3, pushed=0, push_failed=3, conflicted=1),
        ]

        alerts = ops_digest.snapshot_freshness(events, now)

        self.assertEqual(len(alerts), 2)
        self.assertIn("원격 미반영", alerts[0])
        self.assertIn("pull 충돌", alerts[1])

    def test_snapshot_freshness_ignores_machines_that_never_ran(self):
        now = datetime.datetime.fromisoformat("2026-08-06T21:00:00+09:00")

        self.assertEqual(ops_digest.snapshot_freshness([], now), [])

    def test_snapshot_freshness_catches_single_vault_stuck_behind_other_success(self):
        # 볼트 합산 이벤트라 pushed>0가 경보를 가리는 마스킹 시나리오:
        # 매시 {pushed:1, push_failed:1} = 한 볼트 성공·한 볼트 고착
        now = datetime.datetime.fromisoformat("2026-08-06T21:00:00+09:00")
        events = [
            event("vault-snapshot", "run", ts=f"2026-08-06T{h:02d}:00:00+09:00",
                  committed=1, pushed=1, push_failed=1, conflicted=0)
            for h in range(10, 20)
        ]

        alerts = ops_digest.snapshot_freshness(events, now)

        self.assertEqual(len(alerts), 1)
        self.assertIn("고착 의심", alerts[0])

    def test_snapshot_freshness_quiet_on_transient_push_failures(self):
        now = datetime.datetime.fromisoformat("2026-08-06T21:00:00+09:00")
        events = [
            event("vault-snapshot", "run", ts="2026-08-06T18:00:00+09:00",
                  committed=1, pushed=1, push_failed=1, conflicted=0),
            event("vault-snapshot", "run", ts="2026-08-06T19:00:00+09:00",
                  committed=1, pushed=2, push_failed=0, conflicted=0),
            event("vault-snapshot", "run", ts="2026-08-06T20:00:00+09:00",
                  committed=0, pushed=2, push_failed=0, conflicted=0),
        ]

        self.assertEqual(ops_digest.snapshot_freshness(events, now), [])

    def test_snapshot_freshness_survives_non_numeric_payload(self):
        now = datetime.datetime.fromisoformat("2026-08-06T21:00:00+09:00")
        events = [
            event("vault-snapshot", "run", ts="2026-08-06T20:00:00+09:00",
                  committed="abc", pushed="", push_failed=0, conflicted=0),
        ]

        self.assertEqual(ops_digest.snapshot_freshness(events, now), [])

    @mock.patch.object(ops_digest.subprocess, "run")
    @mock.patch.object(ops_digest.shutil, "which", return_value="/usr/local/bin/agent-notify")
    @mock.patch.object(ops_digest.os, "access", return_value=True)
    def test_notify_fires_on_freshness_alone(self, _access, _which, run):
        digest = {
            "errors": [],
            "findings_attention": [],
            "sources_silent": [],
            "snapshot_freshness": ["커밋 3건이 24h째 원격 미반영"],
        }

        ops_digest.notify_digest(digest, None)

        command = run.call_args.args[0]
        self.assertIn("attention", command)
        self.assertIn("🧊신선도 1", " ".join(command))

    @mock.patch.object(ops_digest.subprocess, "run")
    @mock.patch.object(ops_digest.shutil, "which", return_value="/usr/local/bin/agent-notify")
    @mock.patch.object(ops_digest.os, "access", return_value=True)
    def test_notify_fires_on_errors_with_attention_and_link(self, _access, _which, run):
        digest = {
            "errors": [event("x", "error")],
            "findings_attention": [],
            "sources_silent": [],
        }

        ops_digest.notify_digest(digest, "/vault/다이제스트.md")

        command = run.call_args.args[0]
        self.assertIn("attention", command)
        joined = " ".join(command)
        self.assertIn("오류 1", joined)
        self.assertIn("obsidian://open", joined)


if __name__ == "__main__":
    unittest.main()
