import importlib.machinery
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "video-summary"
LOADER = importlib.machinery.SourceFileLoader("video_summary", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
video_summary = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(video_summary)


class VideoSummaryTest(unittest.TestCase):
    def test_extracts_video_id_from_supported_youtube_urls(self):
        urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ?t=42",
            "https://www.youtube.com/shorts/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(video_summary.extract_video_id(url), "dQw4w9WgXcQ")

    def test_rejects_non_youtube_urls(self):
        with self.assertRaises(video_summary.VideoSummaryError):
            video_summary.extract_video_id("https://example.com/video")

    def test_parses_vtt_and_collapses_incremental_captions(self):
        vtt = """WEBVTT

00:00:01.000 --> 00:00:03.000
<c>첫 번째 핵심</c>

00:00:01.000 --> 00:00:04.000
첫 번째 핵심 내용입니다

00:00:05.000 --> 00:00:07.000
두 번째 내용입니다

00:00:05.000 --> 00:00:08.000
두 번째 내용입니다
"""

        cues = video_summary.parse_vtt(vtt)

        self.assertEqual(len(cues), 2)
        self.assertEqual(cues[0].text, "첫 번째 핵심 내용입니다")
        self.assertEqual(cues[0].start_seconds, 1.0)
        self.assertEqual(cues[0].end_seconds, 4.0)
        self.assertEqual(cues[1].text, "두 번째 내용입니다")
        self.assertEqual(cues[1].end_seconds, 8.0)

    def test_compacts_cues_while_preserving_time_ranges(self):
        cues = [
            video_summary.Cue(0, 5, "첫 문장입니다."),
            video_summary.Cue(5, 10, "두 번째 문장입니다."),
            video_summary.Cue(70, 75, "시간이 떨어진 문장입니다."),
        ]

        segments = video_summary.compact_cues(cues, max_chars=100, max_gap_seconds=10)

        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0].start_seconds, 0)
        self.assertEqual(segments[0].end_seconds, 10)
        self.assertIn("첫 문장입니다.", segments[0].text)
        self.assertIn("두 번째 문장입니다.", segments[0].text)

    def test_renders_timestamp_links_and_cache_metadata(self):
        metadata = {
            "video_id": "abc123",
            "source_url": "https://youtu.be/abc123",
            "title": "테스트 영상",
            "channel": "테스트 채널",
            "transcript_hash": "sha256:deadbeef",
            "summary_version": "1",
            "model": "codex-default",
            "input_tokens": 100,
            "output_tokens": 20,
        }
        summary = {
            "overview": "전체 요약입니다.",
            "key_points": [
                {
                    "title": "핵심 주장",
                    "summary": "핵심 설명입니다.",
                    "start": "00:03:12",
                    "end": "00:05:40",
                }
            ],
        }

        markdown = video_summary.render_markdown(metadata, summary)

        self.assertIn("transcript_hash: \"sha256:deadbeef\"", markdown)
        self.assertIn("[00:03:12–00:05:40](https://youtu.be/abc123?t=192)", markdown)
        self.assertIn("### 핵심 주장", markdown)

    def test_finds_matching_cached_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            cached = output_dir / "테스트 영상 [abc123].md"
            cached.write_text(
                """---
video_id: "abc123"
transcript_hash: "sha256:deadbeef"
summary_version: "1"
---
""",
                encoding="utf-8",
            )

            result = video_summary.find_cached_summary(
                output_dir,
                video_id="abc123",
                transcript_hash="sha256:deadbeef",
                summary_version="1",
            )

            self.assertEqual(result, cached)

    @mock.patch.object(video_summary.shutil, "which", return_value="/fake/codex")
    @mock.patch.object(video_summary.subprocess, "run")
    def test_runs_codex_with_schema_and_extracts_usage(self, run, _which):
        response = {
            "overview": "전체 요약입니다.",
            "key_points": [
                {
                    "title": "핵심",
                    "summary": "설명",
                    "start": "00:00:01",
                    "end": "00:00:03",
                }
            ],
        }

        def fake_run(command, **kwargs):
            output_index = command.index("--output-last-message") + 1
            Path(command[output_index]).write_text(
                json.dumps(response, ensure_ascii=False), encoding="utf-8"
            )
            stdout = json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "input_tokens": 120,
                        "cached_input_tokens": 20,
                        "output_tokens": 30,
                    },
                }
            )
            return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

        run.side_effect = fake_run

        result, usage = video_summary.run_codex(
            "prompt", video_summary.FINAL_SCHEMA, model=None
        )

        self.assertEqual(result, response)
        self.assertEqual(usage["input_tokens"], 120)
        self.assertEqual(usage["cached_input_tokens"], 20)
        self.assertEqual(usage["output_tokens"], 30)
        command = run.call_args.args[0]
        self.assertIn("--ephemeral", command)
        self.assertIn("--ignore-user-config", command)
        self.assertIn("read-only", command)
        self.assertEqual(run.call_args.kwargs["input"], "prompt")

    @mock.patch.object(video_summary, "summarize_transcript")
    @mock.patch.object(video_summary, "fetch_youtube_data")
    def test_main_writes_note_then_reuses_cache(self, fetch, summarize):
        fetch.return_value = (
            {
                "id": "dQw4w9WgXcQ",
                "title": "테스트 영상",
                "channel": "테스트 채널",
                "upload_date": "20260716",
                "duration": 30,
            },
            """WEBVTT

00:00:01.000 --> 00:00:05.000
중요한 첫 번째 내용입니다.

00:00:06.000 --> 00:00:10.000
중요한 두 번째 내용입니다.
""",
        )
        summarize.return_value = (
            {
                "overview": "전체 요약입니다.",
                "key_points": [
                    {
                        "title": "핵심",
                        "summary": "핵심 설명입니다.",
                        "start": "00:00:01",
                        "end": "00:00:10",
                    }
                ],
            },
            {"input_tokens": 120, "output_tokens": 30},
            "single-pass",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            arguments = [
                "https://youtu.be/dQw4w9WgXcQ",
                "--output-dir",
                temp_dir,
            ]
            self.assertEqual(video_summary.main(arguments), 0)
            notes = list(Path(temp_dir).glob("*.md"))
            self.assertEqual(len(notes), 1)
            note = notes[0].read_text(encoding="utf-8")
            self.assertIn('input_tokens: 120', note)
            self.assertIn('transcript_hash: "sha256:', note)

            summarize.reset_mock()
            self.assertEqual(video_summary.main(arguments), 0)
            summarize.assert_not_called()


if __name__ == "__main__":
    unittest.main()
