#!/usr/bin/env python3
"""Clova Note 전사본 전처리 — 모델 호출 0.

메타 추출 · 연속 발화 병합 · 글로서리 결정적 치환 · 추임새 제거.
원본은 절대 수정하지 않는다. 결과는 stdout(또는 --out), 리포트는 stderr.

usage:
    prep.py TRANSCRIPT [--glossary PATH] [--out PATH]
    prep.py TRANSCRIPT --meta-only
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# 헤더: "2026.08.05 수 오전 10:09 ・ 42분 0초"
HEADER_RE = re.compile(
    r"^(?P<y>\d{4})\.(?P<m>\d{2})\.(?P<d>\d{2})\s+"
    r"(?P<weekday>[월화수목금토일])\s+"
    r"(?P<ampm>오전|오후)\s+(?P<hh>\d{1,2}):(?P<mm>\d{2})"
    r"(?:\s*[・·]\s*(?P<duration>.+?))?\s*$"
)

# 발화 블록 머리: "참석자 3 09:44" / "참석자 3 1:09:44"
SPEAKER_RE = re.compile(r"^(?P<speaker>참석자\s*\d+|[^\s]{1,20})\s+(?P<ts>\d{1,2}:\d{2}(?::\d{2})?)\s*$")

FOOTER_RE = re.compile(r"^\s*clovanote\.naver\.com\s*$")

# 단독으로 있으면 의미가 없는 추임새 줄. 보수적으로만.
FILLER_RE = re.compile(
    r"^(?:"
    r"[네넵넹어엄음아앙오와으흠]{1,4}"
    r"|(?:네|어|음|아|응|예)(?:[\s.]+(?:네|어|음|아|응|예))*"
    r"|그[.]{0,3}"
    r"|저[.]{0,3}"
    r"|뭐[.]{0,3}"
    r"|이제[.]{0,3}"
    r"|그니까|그러니까|그러면|그래서|하여튼|아무튼"
    r")[.…!?~\s]*$"
)


def parse_glossary(path):
    """`표준어: 오인식1, 오인식2` 한 줄에 한 용어.

    `?` 접두사가 붙은 줄은 **치환하지 않고** 발견만 보고한다
    (`오류`처럼 정상 단어와 겹쳐 자동 치환이 위험한 경우).
    반환: (replace_map, review_map) — 둘 다 {오인식: 표준어}
    """
    replace_map, review_map = {}, {}
    if not path or not Path(path).exists():
        return replace_map, review_map

    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("---"):
            continue
        if ":" not in line:
            continue
        canonical, variants = line.split(":", 1)
        canonical = canonical.strip()
        review_only = canonical.startswith("?")
        if review_only:
            canonical = canonical.lstrip("?").strip()
        if not canonical:
            continue
        target = review_map if review_only else replace_map
        for variant in variants.split(","):
            variant = variant.strip()
            if variant and variant != canonical:
                target[variant] = canonical
    return replace_map, review_map


def build_pattern(mapping):
    """긴 오인식부터 매칭되도록 정렬한 단일 alternation.

    단일 패스 치환이라 치환 결과가 다시 치환되는 연쇄가 일어나지 않는다.
    """
    if not mapping:
        return None
    keys = sorted(mapping, key=len, reverse=True)
    return re.compile("|".join(re.escape(k) for k in keys))


def parse_transcript(text):
    text = text.lstrip("﻿")
    lines = text.splitlines()

    meta = {"title": None, "date": None, "weekday": None,
            "start": None, "duration": None, "owner": None}
    idx = 0

    # 헤더 영역: 제목 / 날짜줄 / 소유자. 첫 발화 블록 전까지만 훑는다.
    while idx < len(lines) and idx < 10:
        line = lines[idx].strip()
        if SPEAKER_RE.match(line):
            break
        if line:
            m = HEADER_RE.match(line)
            if m:
                hh = int(m.group("hh")) % 12
                if m.group("ampm") == "오후":
                    hh += 12
                meta["date"] = f"{m.group('y')}-{m.group('m')}-{m.group('d')}"
                meta["weekday"] = m.group("weekday")
                meta["start"] = f"{hh:02d}:{m.group('mm')}"
                meta["duration"] = (m.group("duration") or "").strip() or None
            elif meta["title"] is None:
                meta["title"] = line
            elif meta["owner"] is None:
                meta["owner"] = line
        idx += 1

    blocks = []  # [{speaker, ts, lines: []}]
    current = None
    for line in lines[idx:]:
        stripped = line.strip()
        if FOOTER_RE.match(stripped):
            continue
        m = SPEAKER_RE.match(stripped)
        if m:
            current = {"speaker": m.group("speaker").replace(" ", " ").strip(),
                       "ts": m.group("ts"), "lines": []}
            blocks.append(current)
        elif stripped and current is not None:
            current["lines"].append(stripped)

    return meta, blocks


def merge_consecutive(blocks):
    """연속된 동일 화자 블록을 하나로 합친다. 타임스탬프는 첫 블록 것을 쓴다."""
    merged = []
    for block in blocks:
        if merged and merged[-1]["speaker"] == block["speaker"]:
            merged[-1]["lines"].extend(block["lines"])
        else:
            merged.append(dict(block, lines=list(block["lines"])))
    return merged


def strip_fillers(blocks):
    removed = 0
    kept = []
    for block in blocks:
        lines = []
        for line in block["lines"]:
            if FILLER_RE.match(line):
                removed += 1
                continue
            lines.append(line)
        if lines:
            kept.append(dict(block, lines=lines))
        else:
            removed += 0  # 블록 전체가 추임새면 블록째 사라진다
    return kept, removed


def apply_glossary(blocks, mapping):
    pattern = build_pattern(mapping)
    if pattern is None:
        return blocks, Counter()

    hits = Counter()

    def sub(m):
        found = m.group(0)
        canonical = mapping[found]
        hits[(canonical, found)] += 1
        return canonical

    for block in blocks:
        block["lines"] = [pattern.sub(sub, line) for line in block["lines"]]
    return blocks, hits


def scan_review(blocks, mapping):
    pattern = build_pattern(mapping)
    if pattern is None:
        return Counter()
    hits = Counter()
    for block in blocks:
        for line in block["lines"]:
            for found in pattern.findall(line):
                hits[(mapping[found], found)] += 1
    return hits


def render(meta, blocks, raw_count):
    speakers = sorted({b["speaker"] for b in blocks})
    out = ["---"]
    for key in ("title", "date", "weekday", "start", "duration", "owner"):
        if meta.get(key):
            out.append(f"{key}: {meta[key]}")
    out.append(f"speakers: {len(speakers)}")
    out.append(f"blocks: {len(blocks)}  # 원본 {raw_count}개에서 병합")
    out.append("---")
    out.append("")
    for block in blocks:
        out.append(f"## {block['speaker']} [{block['ts']}]")
        out.extend(block["lines"])
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def report(hits, review_hits, removed, raw_count, final_count):
    def summarize(counter, label):
        by_canonical = {}
        for (canonical, found), n in counter.items():
            by_canonical.setdefault(canonical, []).append((found, n))
        for canonical in sorted(by_canonical, key=lambda c: -sum(n for _, n in by_canonical[c])):
            variants = sorted(by_canonical[canonical], key=lambda x: -x[1])
            detail = ", ".join(f"{v}({n})" for v, n in variants)
            total = sum(n for _, n in variants)
            print(f"[{label}] {canonical} ← {detail}  총 {total}건", file=sys.stderr)

    summarize(hits, "치환")
    if review_hits:
        print("", file=sys.stderr)
        summarize(review_hits, "검토")
        print("  ↑ 정상 단어와 겹쳐 자동 치환하지 않음. 문맥으로 직접 판단할 것.", file=sys.stderr)
    print("", file=sys.stderr)
    print(f"[요약] 블록 {raw_count} → {final_count}, 추임새 {removed}줄 제거, "
          f"치환 {sum(hits.values())}건", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Clova Note 전사본 전처리")
    ap.add_argument("transcript", type=Path)
    ap.add_argument("--glossary", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--meta-only", action="store_true")
    ap.add_argument("--no-filler-strip", action="store_true")
    args = ap.parse_args()

    if not args.transcript.exists():
        sys.exit(f"전사본을 찾을 수 없음: {args.transcript}")

    text = args.transcript.read_text(encoding="utf-8")
    meta, blocks = parse_transcript(text)
    raw_count = len(blocks)

    if not blocks:
        sys.exit(f"발화 블록을 찾지 못함. Clova Note 형식이 맞는지 확인: {args.transcript}")

    if args.meta_only:
        meta["speakers"] = len({b["speaker"] for b in blocks})
        meta["blocks"] = raw_count
        meta["source"] = str(args.transcript)
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        return

    replace_map, review_map = parse_glossary(args.glossary)
    review_hits = scan_review(blocks, review_map)
    blocks, hits = apply_glossary(blocks, replace_map)
    blocks = merge_consecutive(blocks)
    removed = 0
    if not args.no_filler_strip:
        blocks, removed = strip_fillers(blocks)

    result = render(meta, blocks, raw_count)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(result, encoding="utf-8")
        print(f"[출력] {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(result)

    report(hits, review_hits, removed, raw_count, len(blocks))


if __name__ == "__main__":
    main()
