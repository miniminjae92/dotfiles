import importlib.machinery
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).parents[1] / "bin" / "video-summary"
LOADER = importlib.machinery.SourceFileLoader("video_summary", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
video_summary = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(video_summary)


class VideoSummaryTest(unittest.TestCase):
    @mock.patch.object(video_summary.subprocess, "run")
    def test_reads_named_codex_usage_percent_without_model_call(self, run):
        run.return_value = mock.Mock(
            returncode=0,
            stdout=json.dumps(
                {"google": {"rateLimits": {"primary": {"usedPercent": 37}}}}
            ),
            stderr="",
        )

        used = video_summary.read_used_percent("gcodex")

        self.assertEqual(used, 37)
        run.assert_called_once_with(
            ["gcodex", "usage", "--json"], capture_output=True, text=True
        )

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

    @mock.patch.object(video_summary.shutil, "which", return_value="/fake/yt-dlp")
    @mock.patch.object(video_summary.subprocess, "run")
    def test_lists_channel_videos_with_browser_cookies_and_limit(self, run, _which):
        run.return_value = subprocess.CompletedProcess(
            [],
            0,
            stdout="\n".join(
                [
                    json.dumps(
                        {
                            "id": "public00",
                            "title": "공개 영상",
                            "availability": "public",
                        }
                    ),
                    json.dumps(
                        {
                            "id": "video001",
                            "title": "첫 회원 영상",
                            "availability": "subscriber_only",
                        }
                    ),
                    json.dumps(
                        {
                            "id": "video002",
                            "title": "둘째 회원 영상",
                            "availability": "subscriber_only",
                        }
                    ),
                ]
            ),
            stderr="",
        )

        videos = video_summary.list_channel_videos(
            "https://www.youtube.com/@example/videos",
            cookies_from_browser="chrome:Profile 1",
            max_videos=2,
            members_only=True,
        )

        self.assertEqual([video["id"] for video in videos], ["video001", "video002"])
        command = run.call_args.args[0]
        self.assertIn("--cookies-from-browser", command)
        self.assertEqual(command[command.index("--cookies-from-browser") + 1], "chrome:Profile 1")
        self.assertNotIn("--playlist-end", command)

    @mock.patch.object(video_summary.shutil, "which", return_value="/fake/yt-dlp")
    @mock.patch.object(video_summary.subprocess, "run")
    def test_fetches_subtitles_with_browser_cookies(self, run, _which):
        def fake_run(command, **kwargs):
            Path(kwargs["cwd"], "dQw4w9WgXcQ.ko.vtt").write_text(
                "WEBVTT\n", encoding="utf-8"
            )
            metadata = {
                "id": "dQw4w9WgXcQ",
                "title": "회원 영상",
                "channel": "테스트 채널",
                "duration": 60,
            }
            return subprocess.CompletedProcess(
                command, 0, stdout=json.dumps(metadata), stderr=""
            )

        run.side_effect = fake_run

        video_summary.fetch_youtube_data(
            "https://youtu.be/dQw4w9WgXcQ",
            cookies_from_browser="safari",
        )

        command = run.call_args.args[0]
        self.assertIn("--cookies-from-browser", command)
        self.assertEqual(command[command.index("--cookies-from-browser") + 1], "safari")

    @mock.patch.object(video_summary.shutil, "which", return_value="/fake/yt-dlp")
    @mock.patch.object(video_summary.subprocess, "run")
    def test_batch_metadata_resolution_reuses_one_cookie_session(self, run, _which):
        metadata = {
            "id": "member01",
            "title": "회원 영상",
            "availability": "subscriber_only",
        }
        run.return_value = subprocess.CompletedProcess(
            [], 0, stdout=json.dumps(metadata), stderr=""
        )

        resolved, stderr = video_summary.fetch_video_metadata_batch(
            [
                {
                    "id": "member01",
                    "url": "https://youtu.be/member01",
                }
            ],
            cookies_from_browser="chrome:Default",
        )

        self.assertEqual(resolved["member01"]["availability"], "subscriber_only")
        self.assertEqual(stderr, "")
        command = run.call_args.args[0]
        self.assertIn("--batch-file", command)
        self.assertIn("--cookies-from-browser", command)
        self.assertIn("https://youtu.be/member01", run.call_args.kwargs["input"])

    @mock.patch.object(video_summary.shutil, "which", return_value="/fake/yt-dlp")
    @mock.patch.object(video_summary.subprocess, "run")
    def test_batch_metadata_resolution_keeps_partial_run_recoverable(self, run, _which):
        run.return_value = subprocess.CompletedProcess(
            [], 1, stdout="", stderr="ERROR: Video unavailable. This video is private"
        )

        resolved, stderr = video_summary.fetch_video_metadata_batch(
            [{"id": "private1", "url": "https://youtu.be/private1"}],
            cookies_from_browser="chrome:Default",
        )

        self.assertEqual(resolved, {})
        self.assertIn("private", stderr)

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
            "prompt",
            video_summary.FINAL_SCHEMA,
            model=None,
            reasoning_effort="low",
        )

        self.assertEqual(result, response)
        self.assertEqual(usage["input_tokens"], 120)
        self.assertEqual(usage["cached_input_tokens"], 20)
        self.assertEqual(usage["output_tokens"], 30)
        command = run.call_args.args[0]
        self.assertIn("--ephemeral", command)
        self.assertIn("--ignore-user-config", command)
        self.assertIn("read-only", command)
        self.assertIn('model_reasoning_effort="low"', command)
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

    @mock.patch.object(video_summary, "process_video")
    @mock.patch.object(video_summary, "list_channel_videos")
    def test_channel_mode_skips_existing_and_continues_after_failure(
        self, list_videos, process
    ):
        list_videos.return_value = [
            {"id": "cached01", "title": "기존 영상"},
            {"id": "failed02", "title": "실패 영상"},
            {"id": "success3", "title": "성공 영상"},
        ]
        process.side_effect = [
            video_summary.VideoSummaryError("자막 없음"),
            {"video_id": "success3", "title": "성공 영상", "status": "dry-run"},
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            (output_dir / "기존 영상 [cached01].md").write_text(
                '---\nvideo_id: "cached01"\nsummary_version: "1-detailed"\n'
                'availability: "subscriber_only"\n---\n',
                encoding="utf-8",
            )
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                result = video_summary.main(
                    [
                        "https://www.youtube.com/@example/videos",
                        "--channel",
                        "--members-only",
                        "--cookies-from-browser",
                        "chrome:Default",
                        "--dry-run",
                        "--output-dir",
                        temp_dir,
                    ]
                )

        report = json.loads(stdout.getvalue())
        self.assertEqual(result, 1)
        self.assertEqual(report["counts"], {"cached": 1, "dry-run": 1, "failed": 1})
        self.assertEqual(process.call_count, 2)
        process.assert_any_call(
            "https://youtu.be/failed02",
            mock.ANY,
            skip_existing=False,
        )

    @mock.patch.object(video_summary, "process_video")
    @mock.patch.object(video_summary, "list_channel_videos")
    def test_channel_list_only_does_not_fetch_transcripts(self, list_videos, process):
        list_videos.return_value = [
            {
                "id": "video001",
                "title": "첫 영상",
                "availability": "subscriber_only",
            }
        ]
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            result = video_summary.main(
                [
                    "https://www.youtube.com/@example/videos",
                    "--channel",
                    "--members-only",
                    "--list-only",
                    "--cookies-from-browser",
                    "chrome:Default",
                ]
            )

        report = json.loads(stdout.getvalue())
        self.assertEqual(result, 0)
        self.assertEqual(report["items"][0]["status"], "listed")
        process.assert_not_called()

    def test_members_only_requires_browser_cookies(self):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = video_summary.main(
                [
                    "https://youtu.be/member01",
                    "--members-only",
                ]
            )

        self.assertEqual(result, 1)
        self.assertIn("--cookies-from-browser", stderr.getvalue())

    def test_detailed_prompt_preserves_substantive_information(self):
        prompt = video_summary.final_summary_prompt("[00:00:00-00:00:10] 내용", "detailed")

        self.assertIn("정보 손실을 최소화", prompt)
        self.assertIn("수치", prompt)
        self.assertIn("예외", prompt)
        self.assertIn("질의응답", prompt)

    @mock.patch.object(video_summary, "summarize_transcript")
    @mock.patch.object(video_summary, "fetch_youtube_data")
    def test_members_only_filters_resolved_public_video(self, fetch, summarize):
        fetch.return_value = (
            {
                "id": "public01",
                "title": "공개 영상",
                "availability": "public",
                "duration": 10,
            },
            """WEBVTT

00:00:01.000 --> 00:00:05.000
공개 영상 내용입니다.
""",
        )
        args = video_summary.build_parser().parse_args(
            [
                "https://youtu.be/public01",
                "--channel",
                "--members-only",
                "--cookies-from-browser",
                "chrome:Default",
            ]
        )
        args.summary_mode = "detailed"

        result = video_summary.process_video(
            "https://youtu.be/public01", args, skip_existing=False
        )

        self.assertEqual(result["status"], "filtered")
        summarize.assert_not_called()

    @mock.patch.object(video_summary, "process_video")
    @mock.patch.object(video_summary, "list_channel_videos")
    def test_members_only_defaults_to_all_videos_and_detailed_summary(
        self, list_videos, process
    ):
        list_videos.return_value = [
            {
                "id": "member01",
                "title": "회원 영상",
                "availability": "subscriber_only",
            }
        ]
        process.return_value = {
            "video_id": "member01",
            "title": "회원 영상",
            "status": "dry-run",
        }
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            result = video_summary.main(
                [
                    "https://www.youtube.com/@example/videos",
                    "--channel",
                    "--members-only",
                    "--cookies-from-browser",
                    "chrome:Default",
                    "--dry-run",
                ]
            )

        self.assertEqual(result, 0)
        self.assertEqual(list_videos.call_args.kwargs["max_videos"], 0)
        self.assertTrue(list_videos.call_args.kwargs["members_only"])
        process_args = process.call_args.args[1]
        self.assertEqual(process_args.summary_mode, "detailed")
        self.assertEqual(process_args.model, "gpt-5.6-luna")
        self.assertEqual(process_args.reasoning_effort, "low")

    @mock.patch.object(video_summary, "fetch_video_metadata_batch")
    @mock.patch.object(video_summary, "fetch_flat_entries")
    def test_discovers_member_candidates_across_playlists_without_public_duplicates(
        self, fetch, fetch_metadata
    ):
        def fake_fetch(url, **_kwargs):
            if url.endswith(("/videos", "/streams", "/shorts")):
                return (
                    [{"id": "public01", "title": "공개", "availability": "public"}]
                    if url.endswith("/videos")
                    else []
                )
            if url.endswith("/membership"):
                return [{"id": "member01", "title": "회원 1"}]
            if url.endswith("/community"):
                return [
                    {"id": "public01", "title": "공개"},
                    {"id": "member02", "title": "회원 2"},
                ]
            if url.endswith("/playlists"):
                return [{"id": "PL12345678", "title": "강좌"}]
            if "playlist?list=PL12345678" in url:
                return [
                    {"id": "public01", "title": "공개"},
                    {"id": "member02", "title": "회원 2"},
                    {"id": "member03", "title": "회원 3"},
                ]
            self.fail(f"unexpected URL: {url}")

        fetch.side_effect = fake_fetch
        fetch_metadata.return_value = (
            {
                video_id: {
                    "id": video_id,
                    "title": f"resolved {video_id}",
                    "availability": "subscriber_only",
                }
                for video_id in ("member01", "member02", "member03")
            },
            "",
        )

        videos, warnings = video_summary.discover_channel_member_candidates(
            "https://www.youtube.com/@example/videos",
            cookies_from_browser="chrome:Default",
            max_videos=0,
        )

        self.assertEqual([video["id"] for video in videos], ["member01", "member02", "member03"])
        self.assertEqual(warnings, [])
        self.assertEqual(len(videos[1]["playlists"]), 1)
        self.assertEqual(videos[1]["playlists"][0]["position"], 2)

    def test_writes_playlist_indexes_linking_single_source_notes(self):
        videos = [
            {
                "id": "member01",
                "title": "회원 영상",
                "playlists": [
                    {
                        "id": "PL12345678",
                        "title": "운영체제",
                        "url": "https://www.youtube.com/playlist?list=PL12345678",
                        "position": 4,
                    }
                ],
            }
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            note = Path(temp_dir) / "회원 영상 [member01].md"
            note.write_text("# note\n", encoding="utf-8")
            written = video_summary.write_playlist_indexes(
                videos,
                [
                    {
                        "video_id": "member01",
                        "status": "summarized",
                        "path": str(note),
                    }
                ],
                Path(temp_dir),
            )

            self.assertEqual(len(written), 2)
            playlist = Path(written[1]).read_text(encoding="utf-8")
            overview = Path(written[0]).read_text(encoding="utf-8")
            self.assertIn("4. [[회원 영상 [member01]|회원 영상]]", playlist)
            self.assertIn("운영체제", overview)

    @mock.patch.object(video_summary, "write_playlist_indexes")
    @mock.patch.object(video_summary, "process_video")
    @mock.patch.object(video_summary, "load_member_inventory")
    def test_member_channel_dry_run_does_not_write_indexes(
        self, load_inventory, process_video, write_indexes
    ):
        load_inventory.return_value = (
            [
                {
                    "id": "member01",
                    "title": "회원 영상",
                    "url": "https://youtu.be/member01",
                    "playlists": [],
                }
            ],
            [],
        )
        process_video.return_value = {
            "video_id": "member01",
            "title": "회원 영상",
            "status": "dry-run",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                result = video_summary.main(
                    [
                        "https://www.youtube.com/@example",
                        "--discover-channel-members",
                        "--cookies-from-browser",
                        "chrome:Default",
                        "--dry-run",
                        "--output-dir",
                        temp_dir,
                    ]
                )

        self.assertEqual(result, 0)
        write_indexes.assert_not_called()

    def test_member_inventory_round_trip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "Playlists" / ".member-inventory.json"
            videos = [{"id": "member01", "title": "회원 영상", "playlists": []}]
            video_summary.save_member_inventory(
                path,
                source_url="https://www.youtube.com/@example",
                videos=videos,
                warnings=[],
            )

            loaded = video_summary.load_member_inventory(path)

            self.assertEqual(loaded, (videos, []))

    @mock.patch.object(video_summary, "run_channel", return_value=0)
    def test_discover_channel_members_implies_member_channel_defaults(self, run_channel):
        result = video_summary.main(
            [
                "https://www.youtube.com/@example",
                "--discover-channel-members",
                "--cookies-from-browser",
                "chrome:Default",
            ]
        )

        self.assertEqual(result, 0)
        args = run_channel.call_args.args[0]
        self.assertTrue(args.channel)
        self.assertTrue(args.members_only)
        self.assertEqual(args.max_videos, 0)
        self.assertEqual(args.summary_mode, "detailed")
        self.assertEqual(args.model, "gpt-5.6-luna")


if __name__ == "__main__":
    unittest.main()
