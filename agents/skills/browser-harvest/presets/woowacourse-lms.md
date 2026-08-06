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
