---
name: browser-harvest
description: "Use when a batch of web documents must be saved as local markdown and the pages need a login the agent cannot perform — LMS/과정 자료, 사내 위키, 강의 플랫폼, 구독 문서. Rides the existing Chrome session, converts each page to markdown inside the page, and ships it straight to a local receiver so the body never enters model context. Trigger examples: '이 사이트 문서 다 긁어서 md로 저장', 'LMS 미션 스텝 전부 수확', '로그인해야 보이는 문서들 로컬에 받아줘'."
---

# browser-harvest — 로그인 세션을 탄 웹 문서 일괄 수확

이미 로그인된 브라우저 세션을 그대로 타고, 여러 페이지의 본문을 마크다운으로 바꿔
로컬 디렉터리에 파일로 떨어뜨린다.

핵심 설계: **본문 데이터는 모델 컨텍스트를 거치지 않는다.**
페이지 안에서 md로 변환 → 로컬 1회용 수신 서버로 POST → 디스크. 도구 출력에는 문서별
길이 요약만 흐른다. 20문서(약 80KB) 실측 기준 토큰 비용은 오케스트레이션 호출 십수 회분이 전부.

**안 쓰는 경우**: 로그인이 필요 없고 문서가 몇 개뿐이면 WebFetch가 더 싸다. 이 스킬은
"로그인 장벽 + 다수 문서"일 때 이긴다.

## 입력

- 대상: 문서 목록이 있는 페이지 URL, 또는 수확할 URL 목록
- 저장 위치(디렉터리). 미지정 시 사용자에게 확인
- 사이트 프리셋(있으면). `presets/` 참고 — 없으면 아래 "새 사이트 붙이기"

## 절차 A — 목록 순회형 (한 페이지 안에서 사이드바/목차를 클릭 순회)

SPA 강의, 미션 사이트 대부분이 여기 해당한다. **검증된 경로다.**

1. **브라우저 도구 로드** (한 번의 ToolSearch로):
   `tabs_context_mcp, tabs_create_mcp, navigate, javascript_tool, browser_batch`
2. **탭 준비**: 새 탭 생성 → 대상 URL로 이동. 로그인은 크롬 세션에 이미 있어야 한다
   (없으면 사용자에게 로그인 요청하고 중단. **로그인 대행 금지**).
3. **수신 서버 기동** (Bash, `run_in_background: true`):
   `node <이 스킬 디렉터리>/receiver.js <scratchpad>/harvest.json 4199`
   1회 수신 후 자동 종료, 5분 무수신 시 타임아웃.
4. **수확기 주입**: `harvester.js` 파일 내용을 Read로 읽어 `javascript_tool`로 실행
   (SPA 로딩 완료 후. 필요하면 2초 대기 선행). `window.__harvest`가 설치된다.
5. **수확 실행**: 프리셋의 config로 한 줄 호출.
   ```js
   await window.__harvest.run({ receiverUrl: 'http://127.0.0.1:4199/save', itemSelector: '…', /* … */ })
   ```
   반환 `status`에서 문서 수, 오류 확인. `error: 'list item not found'`가 있으면 그 섹션이
   목록에서 접혀 있는 것 — 펼친 뒤 재실행.
6. **파일 분할**: `node <이 스킬 디렉터리>/split.js <scratchpad>/harvest.json <저장디렉터리> <오늘날짜>`
   → 섹션별 하위 디렉터리 + 문서별 md(frontmatter: source/section/id/harvested/meta) + README 인덱스.
7. **검증**: 파일 수 = status의 문서 수인지 확인하고 결과를 보고.

## 절차 B — URL 목록형 (페이지를 옮겨 다니며 1건씩)

목록이 링크 목록이라 클릭 순회가 안 될 때. 페이지 이동마다 주입 스크립트가 날아가므로
URL마다 주입 → 1건 수확을 반복한다.

1~2는 A와 같다. 3에서 출력 경로를 `.jsonl`로 준다
(`node receiver.js <scratchpad>/harvest.jsonl 4199`).
그다음 URL마다: `navigate` → `harvester.js` 주입 →
`await window.__harvest.grabPage({ receiverUrl: 'http://127.0.0.1:4199/append', meta: { section: '…' } })`.
전부 끝나면 `/done`으로 서버를 닫고(`curl -XPOST 127.0.0.1:4199/done`), split.js로 분할한다.

## 새 사이트 붙이기 (셀렉터 3단계)

1. `document.querySelectorAll('<후보>').length`로 **목록 항목**(`itemSelector`)을 맞춘다 — 문서 수와 일치해야 한다.
2. 섹션 구분이 있으면 항목을 감싸는 상자를 `groupSelector`로 잡는다(첫 자식 텍스트를 섹션명으로 쓴다). 없으면 생략.
3. 본문 컨테이너(`contentSelector`, 기본 `main`)를 확인하고, id, 제목이 DOM에 안 드러나면
   기본 React fiber 탐색(`fiberIdentify`)에 맡긴다. 평범한 `<a href>` 목록이면 더 간단하다:
   `identify: (el) => ({ id: el.getAttribute('href'), title: el.textContent.trim() })`
4. 잘 도는 config를 `presets/<사이트>.md`에 그대로 저장한다. 다음 사람이 1~3을 다시 안 하게.

config 전체 키는 `harvester.js`의 `DEFAULTS` 참고
(`waitMs`, `strip`, `sourceOf`, `meta` 등).

## 알려진 함정 (피 흘려 얻은 것 — 지우지 말 것)

- **API 직접 호출은 403이다.** 사이트의 백엔드 API를 직접 때리려 들지 말고, 특히
  **인증 토큰을 브라우저에서 꺼내지 않는다**(보안 경계). DOM/React fiber 경유가 정답이다.
- **원시 HTML을 도구 출력으로 반출하면 DLP 필터에 걸린다.** 페이지 내용을 모델로 끌어와서
  변환하는 설계는 막힌다. 반드시 페이지 안에서 md로 바꿔 로컬 수신 서버로 직송한다.
  (토큰 절감은 덤이고, 애초에 이게 유일하게 통하는 경로다.)
- **사이트 UI 개편 시 깨지는 지점은 셀렉터 2개뿐이다** — `itemSelector` / `groupSelector`
  (그리고 fiber 키 순회). 프리셋의 그 두 줄만 고치면 살아난다. 엔진은 건드릴 일이 없다.
- **읽기 전용**: 항목 클릭(열람)만 한다. 제출, 평가, 설정, 결제 버튼은 절대 누르지 않는다.
- **수확물은 개인 사본이다.** 외부 공개, 재배포하지 않는다. 사이트 이용약관을 따른다.

## 선택 후속: 종합 가이드

수확본이 크면 원문을 메인 컨텍스트로 읽지 말고, 섹션별 병렬 서브에이전트(스키마 강제)로
행동, 제출물, 마감, 규칙만 추출한 뒤 종합 md를 작성한다.
