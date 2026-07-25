---
name: dref-save
description: "Use when the user asks to save a URL/design reference to dref during a session — e.g. '이거 dref에 저장해줘', '이 사이트 레퍼런스로 등록', or shares a design link worth keeping. Saves via the local dref API (port 4180) with type/tags/note classification."
---

# dref-save

디자인 레퍼런스를 로컬 dref 라이브러리(`~/projects/my/dref`)에 저장한다.

## 절차

1. URL·제목·분류를 정한다. 사용자가 안 준 것은 대화 맥락과 페이지 내용에서 추론한다.
   - `type` (필수, 8종): `landing | dashboard | component | typography | color | animation | css-technique | ux-pattern`
   - `tags`: 자유 어휘 소문자 배열 (예: `["dark", "pricing"]`)
   - `note`: "왜 좋은가" 한 줄 — 사용자가 말한 이유를 그대로 담는 게 최선. 없으면 짧은 추정 + 사용자가 다듬게 언급.
2. 저장:
   ```sh
   curl -sX POST http://127.0.0.1:4180/api/items -H 'content-type: application/json' \
     -d '{"url":"<URL>","title":"<제목>","type":"<type>","tags":["…"],"note":"<왜 좋은가>","source":"claude-session"}'
   ```
3. 응답 처리:
   - `201 {"id": …}` → 저장됨. 스크린샷은 서버가 배경에서 캡처한다고 알린다.
   - `409 duplicate url` → 이미 있음. `curl -s 'http://127.0.0.1:4180/api/items?q=<검색어>'`로 기존 아이템을 찾아 보여준다.
   - 연결 거부 → 서버가 죽어 있다: `launchctl kickstart gui/$(id -u)/com.miniminjae.dref` 후 재시도.

## 주의

- 저장 후 분류를 고치려면: `curl -sX PATCH http://127.0.0.1:4180/api/items/<id> -H 'content-type: application/json' -d '{"tags":"…","note":"…"}'`
- 여러 URL을 한 번에 저장해달라면 각각 POST(중복은 409로 자연 스킵).
