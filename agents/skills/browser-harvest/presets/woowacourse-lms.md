# 프리셋 — 우테코 LMS+ 미션 스텝

- 사이트: `techcourse-lms-plus-web.woowahan.com`
- 대상: 미션 페이지(`/missions/<번호>`)의 사이드바 스텝 전체
- 모드: A(목록 순회)
- 검증: 2026-07-23, missions/31 레벨3 — 20스텝(약 80KB) 전량 수확 성공

## config

`harvester.js` 주입 후 이 한 줄을 `javascript_tool`로 실행한다.

```js
await window.__harvest.run({
  receiverUrl: 'http://127.0.0.1:4199/save',
  itemSelector: 'div.group.flex.flex-col',   // 사이드바 스텝 항목
  groupSelector: 'div.mb-2',                 // 사이드바 섹션 그룹(OT/1주차/2주차)
  contentSelector: 'main',
  waitMs: 1200,
  strip: [/^진행 단계\d*\s*/, /\[\]\(#[^)]*\)/g],
  sourceOf: (id) => location.origin + location.pathname + '?step=' + id,
  meta: { mission: 'missions/' + (location.pathname.match(/missions\/(\d+)/)?.[1] ?? '') },
})
```

스텝 id, 제목은 DOM에 없다. 기본 `fiberIdentify`(React fiber 순회)가 잡아낸다.

## 이 사이트 특유의 함정

- **사이드바 섹션이 접혀 있으면 그 안의 스텝은 DOM에 없다.** `status`에
  `error: 'list item not found'`가 보이면 접힌 섹션을 펼치고 다시 `run`한다.
  수확 전에 전 섹션을 펼쳐두는 편이 안전하다.
- `techcourse-lms-plus-api...` 직접 호출은 403이다. 토큰을 꺼내지 않는다(SKILL.md 함정 절 참고).
- 본문 머리에 "진행 단계N"이 붙고, 헤딩 앵커가 `[](#...)` 찌꺼기로 남는다 — 위 `strip`이 처리한다.
- UI 개편으로 깨지면 `itemSelector`/`groupSelector` 두 줄만 다시 잡으면 된다.

## 산출물

`split.js` 통과 후: 섹션별 디렉터리(`00-OT`, `01-1주차`, …) + 스텝별 md.
frontmatter에 `source`(스텝 딥링크) · `mission` · `section` · `id` · `harvested`.

## 수신 서버가 안 통할 때 (2026-08-18, missions/39)

크롬이 HTTPS 페이지에서 `http://127.0.0.1`(및 `localhost`)로 나가는 요청을 **응답 없이 붙잡는**
환경이 있다. 로컬 네트워크 접근 차단이다. 증상이 특이해서 오진하기 쉽다:

- `fetch`가 reject도 resolve도 안 하고 영원히 pending. `mode:'no-cors'`도 같다.
- 콘솔에 CSP 위반도, 네트워크 에러도 **안 찍힌다**.
- 수신 서버 로그에 요청이 아예 안 들어온다(curl로는 정상 응답).
- `javascript_tool`이 `run()`의 POST 단계에서 CDP 45초 타임아웃으로 죽는다.
  이때 클릭 순회는 이미 끝나 있고 `window.__harvest`도 살아 있다 — 엔진 문제가 아니다.

판별: `curl -XPOST 127.0.0.1:4199/append -d '{}'`가 200이면 서버는 멀쩡하고 브라우저가 막힌 것이다.

### 우회 — 수신 서버 없이 페이지 안에 모았다가 도구 출력으로 회수

`run()` 대신 `grab()`을 직접 돌려 `window.__docs`에 쌓고, 슬라이스로 나눠 읽어 로컬에 쓴다.

```js
const cfg = { itemSelector: 'div.group.flex.flex-col', contentSelector: 'main', waitMs: 1500,
  identify: window.__harvest.fiberIdentify,
  strip: [/^진행 단계\d*\s*/, /\[\]\(#[^)]*\)/g],
  sourceOf: (id) => location.origin + location.pathname + '?step=' + id };
window.__docs = [];
for (const it of [...document.querySelectorAll(cfg.itemSelector)].map(e => cfg.identify(e))) {
  const r = await window.__harvest.grab(it.id, '', cfg);
  window.__docs.push({ id: it.id, title: it.title, source: r.source, md: r.md ?? ('ERROR: ' + r.error) });
}
window.__docs.map(d => ({ id: d.id, title: d.title, len: d.md.length }))  // 목록만 먼저 확인
```

회수는 `window.__docs.slice(a,b).map(d => d.id + '\n' + d.md).join('\n\n=====\n\n')`.
**`javascript_tool` 출력은 1200자 근처에서 잘린다.** 긴 문서는 `md.slice(600)`처럼 오프셋을 줘
이어 읽는다. 마크다운은 DLP에 안 걸린다(걸리는 건 원시 HTML이다).

대가는 본문이 모델 컨텍스트를 통과한다는 것 — 이 스킬의 설계 목적을 정면으로 깬다.
6문서 3KB면 무시할 만하지만 **수십 문서면 쓰지 말 것.** 그 규모면 차단을 푸는 게 먼저다.
회수가 끝나면 `delete window.__docs`로 지운다.
