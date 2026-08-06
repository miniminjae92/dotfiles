---
name: dref-consult
description: "Use when the user asks a design question that should draw on their personal reference library — e.g. '다크모드 대시보드 레퍼런스 보여줘', '가격표 섹션 어떻게 잡을까', 'dref에서 …찾아줘', or any UI/visual design consultation. Searches ~/projects/dref/library (markdown + screenshots) and answers grounded in saved references."
---

# dref-consult

사용자의 개인 디자인 레퍼런스 라이브러리를 근거로 디자인 질문에 답한다.
라이브러리 = `~/projects/dref/library/items/**/item.md` (frontmatter: type/tags + 본문 "왜 좋은가").

## 절차

1. **검색** — 두 경로 중 편한 쪽(둘 다 가능):
   - 파일: `rg -il '<키워드>' ~/projects/dref/library/items --glob 'item.md'`
     축/태그 필터: `rg -l 'type: dashboard' …`
   - FTS API: `curl -s 'http://127.0.0.1:4180/api/items?q=<검색어>&type=<축>&status=approved'`
2. **읽기** — 맞는 아이템의 `item.md`를 Read. 시각 판단이 필요하면 같은 디렉터리의 `shot.jpg`도 Read(이미지 지원).
3. **답변** — 반드시 저장된 아이템을 인용해 답한다: 제목, URL, "왜 좋은가" 주석을 근거로.
   - 라이브러리에 근거가 없으면 없다고 말하고 일반 지식으로 답하되, 그 구분을 명확히.
   - 답하며 발견한 좋은 외부 레퍼런스는 dref-save 스킬로 저장을 제안.

## 주의

- status=rejected 아이템은 근거로 쓰지 않는다(거절된 취향).
- 사용자의 취향 신호는 note(왜 좋은가)에 있다 — 제목보다 note를 우선 근거로.
