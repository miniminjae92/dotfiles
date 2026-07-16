from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOADER = importlib.machinery.SourceFileLoader("kman_module", str(ROOT / "bin/kman"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
assert SPEC is not None
KMAN = importlib.util.module_from_spec(SPEC)
sys.modules[LOADER.name] = KMAN
LOADER.exec_module(KMAN)


class KmanTests(unittest.TestCase):
    def test_candidate_terms_adds_only_unknown_acronyms(self) -> None:
        text = """DESCRIPTION
        The PID belongs to an ABCD worker using TMUX_TMPDIR.
        Send SIGUSR1 to reload it.
        """

        result = KMAN.candidate_terms(text, {"PID", "SIGUSR1"})

        self.assertEqual(list(result), ["ABCD"])
        self.assertEqual(result["ABCD"]["status"], "candidate")

    def test_technical_pieces_protects_commands_and_flags(self) -> None:
        pieces = KMAN.technical_pieces(
            "Run tmux with -L socket-name and inspect pty(4).", "tmux"
        )

        protected = {piece["text"] for piece in pieces if not piece["translate"]}
        self.assertTrue({"tmux", "-L", "pty(4)"}.issubset(protected))

    def test_identity_translation_keeps_body_clean_and_translates_heading(self) -> None:
        source = """NAME

     tmux is a terminal multiplexer used for sessions and windows.
"""

        result, warnings = KMAN.render_translation(
            source,
            "tmux",
            "identity",
            Path(tempfile.gettempdir()),
            Path(tempfile.gettempdir()) / "kman-test-blocks",
        )

        self.assertIn("이름", result)
        self.assertIn("tmux is a terminal multiplexer", result)
        self.assertNotIn("Process Identifier", result)
        self.assertEqual(warnings, [])

    def test_display_width_wraps_korean_to_terminal_columns(self) -> None:
        wrapped = KMAN.wrap_for_terminal("한국어 문장을 " * 40, "     ", width=60)

        self.assertGreater(len(wrapped.splitlines()), 2)
        self.assertTrue(
            all(KMAN.display_width(line) <= 60 for line in wrapped.splitlines())
        )

    def test_protected_terms_restore_exact_case(self) -> None:
        items = [
            {
                "pieces": [
                    {"text": "Run ", "translate": True},
                    {"text": "-c", "translate": False},
                    {"text": " with ", "translate": True},
                    {"text": "tmux", "translate": False},
                ]
            }
        ]

        protected, mappings = KMAN.protect_items(items)
        placeholder_text = "".join(piece["text"] for piece in protected[0]["pieces"])
        restored = KMAN.restore_protected_terms(placeholder_text.upper(), mappings[0])

        self.assertEqual(restored, "RUN -c WITH tmux")

    def test_colorize_highlights_sections_and_options(self) -> None:
        output = KMAN.colorize("설명\n\n     -c shell-command\n")

        self.assertIn("\033[1;36m설명", output)
        self.assertIn("\033[1;33m-c", output)

    def test_reflow_formats_existing_korean_cache_without_translation(self) -> None:
        cached = "     " + ("한국어 문장을 자연스럽게 표시합니다. " * 20) + "\n"

        formatted = KMAN.reflow_for_display(cached)

        self.assertGreater(len(formatted.splitlines()), 2)
        self.assertTrue(
            all(KMAN.display_width(line) <= KMAN.MAN_WIDTH for line in formatted.splitlines())
        )

    def test_legacy_cache_is_reused_before_new_translation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            legacy = cache / "ko.apple.v1.txt"
            legacy.write_text("기존 번역", encoding="utf-8")

            selected = KMAN.legacy_translation_path(cache, "apple")

            self.assertEqual(selected, legacy)

    def test_failed_protection_falls_back_without_caching(self) -> None:
        item = {
            "pieces": [
                {"text": "Run ", "translate": True},
                {"text": "display-panes", "translate": False},
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "block.txt"

            result, warning = KMAN.finalize_translation_item(
                "번역에서 표식이 사라짐",
                {"KMANPH0X1Z": "display-panes"},
                item,
                destination,
            )

            self.assertEqual(result, "Run display-panes")
            self.assertIn("영문 원문", warning or "")
            self.assertFalse(destination.exists())

    def test_successful_block_is_cached_immediately(self) -> None:
        item = {
            "pieces": [
                {"text": "Run ", "translate": True},
                {"text": "tmux", "translate": False},
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "block.txt"

            result, warning = KMAN.finalize_translation_item(
                "실행 KMANPH0X1Z",
                {"KMANPH0X1Z": "tmux"},
                item,
                destination,
            )

            self.assertEqual(result, "실행 tmux")
            self.assertIsNone(warning)
            self.assertEqual(destination.read_text(encoding="utf-8"), result)

    def test_detect_license_for_isc_and_bsd(self) -> None:
        self.assertEqual(
            KMAN.detect_license(
                "Permission to use, copy, modify, and distribute this software"
            ),
            "ISC",
        )
        self.assertEqual(
            KMAN.detect_license(
                '.\\" Redistribution and use in source and binary forms\n.\\" 3. no endorsement'
            ),
            "BSD-3-Clause",
        )

    def test_export_rejects_unknown_license(self) -> None:
        page = KMAN.ManPage(
            name="sample",
            section="1",
            source_path=Path("sample.1"),
            source_text="",
            rendered_text="sample",
            source_hash="abc",
            license_name="UNKNOWN",
            license_notice="",
        )
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(KMAN.KmanError, "공개 허용 목록"):
                KMAN.export_markdown(
                    Path(directory) / "sample.md", page, "번역", {}, {}
                )


if __name__ == "__main__":
    unittest.main()
