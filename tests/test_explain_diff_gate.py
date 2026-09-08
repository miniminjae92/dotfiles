import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / "bin" / "explain-diff-gate"


class ExplainDiffGateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.run_git("init", "-q")
        self.run_git("config", "user.name", "Test")
        self.run_git("config", "user.email", "test@example.com")
        (self.repo / "tracked.txt").write_text("before\n", encoding="utf-8")
        self.run_git("add", "tracked.txt")
        self.run_git("commit", "-q", "-m", "initial")
        (self.repo / "tracked.txt").write_text("after\n", encoding="utf-8")
        self.run_git("add", "tracked.txt")
        self.state = self.root / "state"

    def tearDown(self):
        self.temporary.cleanup()

    def run_git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                              capture_output=True, text=True)

    def run_gate(self, *args):
        env = {
            **os.environ,
            "EXPLAIN_DIFF_DIR": str(self.state / "explain-diff"),
            "OPS_STATE_DIR": str(self.state / "ops"),
        }
        return subprocess.run([str(SCRIPT), *args], cwd=self.repo, env=env,
                              capture_output=True, text=True, check=False)

    def records(self):
        path = self.state / "explain-diff" / "records.jsonl"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    def ops_events(self):
        return list((self.state / "ops" / "events").glob("*.jsonl"))

    def write_document(self, name="explain.html"):
        document = self.state / "explain-diff" / name
        document.parent.mkdir(parents=True, exist_ok=True)
        metadata = self.run_gate("metadata")
        self.assertEqual(metadata.returncode, 0, metadata.stderr)
        document.write_text(f"""<!doctype html>
<html><head><title>변경 설명</title>
{metadata.stdout}</head><body>
<h1>변경 설명</h1>
<h2>배경</h2><p>이 변경 전에는 설명서 승인 기록이 현재 변경과 연결되는지 확인할 수 없어서, 오래된 문서를 다시 써도 게이트가 통과할 위험이 있었습니다.</p>
<h2>직관</h2><p>생성 시점의 저장소와 diff 해시를 문서 안에 넣고, 승인 단계는 그 값을 읽기만 하면 설명서와 현재 변경이 같은 대상을 가리키는지 확인할 수 있습니다.</p>
<h2>코드</h2><p>메타데이터 명령이 현재 staged와 HEAD diff 후보를 출력하고, 게이트는 HTML 구조와 네 설명 단위의 실제 본문을 검증한 뒤 기록만 추가합니다.</p>
<h2>퀴즈</h2><p>첫째, 이전 설명서의 해시가 현재 diff와 다르면 왜 거절될까요? 둘째, ack가 문서를 수정하지 않는 이유는 무엇일까요? 셋째, 메타데이터는 언제 다시 만들어야 할까요?</p>
</body></html>
""", encoding="utf-8")
        return document

    def test_ack_requires_path(self):
        result = self.run_gate("ack")

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.records(), [])
        self.assertEqual(self.ops_events(), [])

    def test_ack_rejects_nonexistent_path_without_recording(self):
        result = self.run_gate("ack", "--path", "missing.html")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("EXPLAIN_DIFF_DIR 아래", result.stderr)
        self.assertEqual(self.records(), [])
        self.assertEqual(self.ops_events(), [])

    def test_ack_rejects_empty_file_without_recording(self):
        document = self.state / "explain-diff" / "empty.html"
        document.parent.mkdir(parents=True)
        document.touch()

        result = self.run_gate("ack", "--path", str(document))

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.records(), [])
        self.assertEqual(self.ops_events(), [])

    def test_ack_records_current_structured_document_without_writing_it(self):
        document = self.write_document()
        before = document.read_bytes()

        result = self.run_gate("ack", "--path", str(document))

        self.assertEqual(result.returncode, 0, result.stderr)
        records = self.records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["action"], "ack")
        self.assertEqual(records[0]["path"], os.path.realpath(document))
        self.assertIn("document_sha256", records[0])
        self.assertEqual(document.read_bytes(), before)

    def test_ack_rejects_minimal_keyword_only_html_even_with_current_metadata(self):
        document = self.state / "explain-diff" / "fake.html"
        document.parent.mkdir(parents=True)
        metadata = self.run_gate("metadata")
        self.assertEqual(metadata.returncode, 0, metadata.stderr)
        document.write_text(f"""<html><head><title>x</title>{metadata.stdout}</head><body>
<h1>x</h1><h2>배경</h2>배경<h2>직관</h2>직관<h2>코드</h2>코드<h2>퀴즈</h2>퀴즈
</body></html>""",
                            encoding="utf-8")

        result = self.run_gate("ack", "--path", str(document))

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.records(), [])

    def test_ack_rejects_stale_document_after_diff_changes(self):
        document = self.write_document("stale.html")
        (self.repo / "tracked.txt").write_text("changed again\n", encoding="utf-8")
        self.run_git("add", "tracked.txt")

        result = self.run_gate("ack", "--path", str(document))

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.records(), [])

    def test_ack_rejects_nonempty_document_outside_state_dir(self):
        document = self.root / "outside.html"
        document.write_text("<html>explanation</html>\n", encoding="utf-8")

        result = self.run_gate("ack", "--path", str(document))

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.records(), [])
        self.assertEqual(self.ops_events(), [])

    def test_ack_rejects_non_html_document_inside_state_dir(self):
        document = self.state / "explain-diff" / "explain.md"
        document.parent.mkdir(parents=True)
        document.write_text("explanation\n", encoding="utf-8")

        result = self.run_gate("ack", "--path", str(document))

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.records(), [])
        self.assertEqual(self.ops_events(), [])

    def test_ack_rejects_symlink_escaping_state_dir(self):
        outside = self.root / "outside.html"
        outside.write_text("<html>explanation</html>\n", encoding="utf-8")
        document = self.state / "explain-diff" / "linked.html"
        document.parent.mkdir(parents=True)
        document.symlink_to(outside)

        result = self.run_gate("ack", "--path", str(document))

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.records(), [])
        self.assertEqual(self.ops_events(), [])

    def test_skip_still_records_without_document(self):
        result = self.run_gate("skip", "docs-only", "--note", "user approved")

        self.assertEqual(result.returncode, 0, result.stderr)
        records = self.records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["action"], "skip")
        self.assertNotIn("path", records[0])


if __name__ == "__main__":
    unittest.main()
