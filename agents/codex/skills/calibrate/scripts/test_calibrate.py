#!/usr/bin/env python3
"""Behavioral tests for the calibrate command wrapper."""

from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest


SCRIPT = Path(__file__).with_name("calibrate.py")


class CalibrateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.state_root = self.root / "state"
        self.log_path = self.root / "invocations.jsonl"
        self.fake_codex = self.root / "fake-codex"
        self.fake_codex.write_text(
            textwrap.dedent(
                f"""\
                #!{sys.executable}
                import json
                import os
                from pathlib import Path
                import sys

                arguments = sys.argv[1:]
                log_path = Path(os.environ["FAKE_CODEX_LOG"])
                codex_home = Path(os.environ["CODEX_HOME"])
                with log_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps({{
                        "arguments": arguments,
                        "codex_home": str(codex_home),
                        "codex_home_mode": codex_home.stat().st_mode & 0o777,
                        "auth_exists": (codex_home / "auth.json").is_file(),
                        "auth_is_symlink": (codex_home / "auth.json").is_symlink(),
                    }}, ensure_ascii=False) + "\\n")

                prompt = arguments[-1]
                isolated = "--ignore-user-config" in arguments
                is_core = "Use this minimum contract:" in prompt
                if os.environ.get("FAKE_CODEX_FAIL_CORE") == "1" and is_core:
                    print("core failure", file=sys.stderr)
                    raise SystemExit(7)
                if is_core:
                    print("후보 둘")
                elif isolated:
                    print("후보 하나")
                else:
                    print("후보 셋")
                """
            ),
            encoding="utf-8",
        )
        self.fake_codex.chmod(
            self.fake_codex.stat().st_mode | stat.S_IXUSR,
        )
        self.environment = os.environ.copy()
        self.environment["FAKE_CODEX_LOG"] = str(self.log_path)
        self.source_codex_home = self.root / "codex-home"
        self.source_codex_home.mkdir()
        (self.source_codex_home / "auth.json").write_text("{}", encoding="utf-8")
        (self.source_codex_home / "config.toml").write_text(
            textwrap.dedent(
                """\
                notify = ["notify-helper"]

                [mcp_servers.alpha]
                command = "alpha"

                [mcp_servers."dotted.name"]
                command = "dotted"
                """
            ),
            encoding="utf-8",
        )
        (self.root / ".git").mkdir()
        (self.root / ".codex").mkdir()
        (self.root / ".codex" / "config.toml").write_text(
            "[mcp_servers.project]\ncommand = 'project'\n",
            encoding="utf-8",
        )
        self.environment["CODEX_HOME"] = str(self.source_codex_home)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def start(self, *extra: str, environment: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(SCRIPT),
            "start",
            "--task",
            "한 문장으로 답해줘.",
            "--cwd",
            str(self.root),
            "--model",
            "test-model",
            "--reasoning-effort",
            "low",
            "--codex-bin",
            str(self.fake_codex),
            "--state-root",
            str(self.state_root),
            "--seed",
            "7",
            "--serial",
            *extra,
        ]
        return subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            env=environment or self.environment,
        )

    def test_start_is_blind_isolated_and_revealable(self) -> None:
        result = self.start()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("## A"), 1)
        self.assertEqual(result.stdout.count("## B"), 1)
        self.assertEqual(result.stdout.count("## C"), 1)
        self.assertNotIn("clean", result.stdout)
        self.assertNotIn("core", result.stdout)
        self.assertNotIn("full", result.stdout)
        for candidate in ("후보 하나", "후보 둘", "후보 셋"):
            self.assertEqual(result.stdout.count(candidate), 1)

        latest_path = self.state_root / "latest.json"
        latest = json.loads(latest_path.read_text(encoding="utf-8"))
        state_path = self.state_root / f"{latest['run_id']}.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(set(state["mapping"]), {"A", "B", "C"})
        self.assertEqual(set(state["mapping"].values()), {"clean", "core", "full"})
        self.assertEqual(self.state_root.stat().st_mode & 0o777, 0o700)
        self.assertEqual(latest_path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(state_path.stat().st_mode & 0o777, 0o600)

        records = [
            json.loads(line)
            for line in self.log_path.read_text(encoding="utf-8").splitlines()
        ]
        invocations = [record["arguments"] for record in records]
        self.assertEqual(len(invocations), 3)
        for invocation in invocations:
            self.assertIn("--ephemeral", invocation)
            self.assertIn("read-only", invocation)
            self.assertIn("test-model", invocation)
            self.assertIn("hooks", invocation)
            self.assertIn("apps", invocation)
            self.assertIn("plugins", invocation)
            self.assertIn("remote_plugin", invocation)
            self.assertIn("multi_agent", invocation)
            self.assertIn("browser_use", invocation)
            self.assertIn("browser_use_external", invocation)
            self.assertIn("computer_use", invocation)
            self.assertIn("image_generation", invocation)
            self.assertIn("in_app_browser", invocation)
            self.assertIn("notify=[]", invocation)
        full_record = next(
            record for record in records if "--ignore-user-config" not in record["arguments"]
        )
        self.assertIn(
            'mcp_servers={"alpha"={enabled=false},"dotted.name"={enabled=false},"project"={enabled=false}}',
            full_record["arguments"],
        )
        self.assertEqual(full_record["codex_home"], str(self.source_codex_home))
        self.assertTrue(full_record["auth_exists"])
        self.assertFalse(full_record["auth_is_symlink"])
        isolated_records = [
            record for record in records if "--ignore-user-config" in record["arguments"]
        ]
        self.assertEqual(len(isolated_records), 2)
        self.assertEqual(len({record["codex_home"] for record in isolated_records}), 1)
        self.assertNotEqual(isolated_records[0]["codex_home"], str(self.source_codex_home))
        for record in isolated_records:
            self.assertEqual(record["codex_home_mode"], 0o700)
            self.assertTrue(record["auth_exists"])
            self.assertTrue(record["auth_is_symlink"])
            self.assertIn(
                'mcp_servers={"project"={enabled=false}}',
                record["arguments"],
            )
        isolated = [item for item in invocations if "--ignore-user-config" in item]
        self.assertEqual(len(isolated), 2)
        for invocation in isolated:
            self.assertIn("--ignore-rules", invocation)
            self.assertIn("project_doc_max_bytes=0", invocation)
            self.assertIn("memories", invocation)
            self.assertIn("personality", invocation)
        core = [item for item in isolated if "Use this minimum contract:" in item[-1]]
        self.assertEqual(len(core), 1)

        reveal = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "reveal",
                "B",
                "--state-root",
                str(self.state_root),
                "--reason",
                "더 자연스럽다",
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(reveal.returncode, 0, reveal.stderr)
        payload = json.loads(reveal.stdout)
        self.assertEqual(payload["choice"], "B")
        self.assertEqual(payload["reason"], "더 자연스럽다")
        self.assertEqual(
            payload["selected_candidate"],
            payload["candidates"]["B"],
        )

    def test_any_failed_profile_aborts_the_comparison(self) -> None:
        environment = self.environment.copy()
        environment["FAKE_CODEX_FAIL_CORE"] = "1"
        result = self.start(environment=environment)
        self.assertEqual(result.returncode, 2)
        self.assertIn("세 후보를 모두 만들지 못했습니다", result.stderr)
        self.assertIn("core failure", result.stderr)
        self.assertFalse((self.state_root / "latest.json").exists())

    def test_reveal_without_state_is_a_clear_error(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "reveal",
                "A",
                "--state-root",
                str(self.state_root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("대기 중인 비교를 찾지 못했습니다", result.stderr)


if __name__ == "__main__":
    unittest.main()
