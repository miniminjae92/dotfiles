# Upstreams — 외부 상류 대장

외부에서 들여오는 것들의 구독 현황판. 3분류(D-014):

- **워크플로** — 스킬로 벤더링해 들여온다 (수정 권리, 수동 diff 갱신)
- **표준** — 벤더링하지 않고 최신 원문을 참조한다 (확인일 관리)
- **도구** — 설치해서 피드백 시스템으로 쓴다

## 워크플로

| upstream | 방식 | 로컬 위치 | 상태 |
| --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 벤더 (스킬별 VENDOR.md) | `agents/skills/` — active 28종 (2026-07-25, 플러그인 v1.2.0 기준·teach는 ed37663) | 시험 기간 (CLAUDE.md 규약) |

- 갱신법: upstream 저장소를 받아 각 스킬의 VENDOR.md 기준 커밋/버전과 diff → 원하는 변경만 반영 → VENDOR.md의 commit·날짜 갱신.
- 수정 현황: `obsidian-vault` 1건 (자동 발동 봉인 — VENDOR.md에 사유 기록). 나머지 27종 무수정.
- 플러그인 구독은 2026-07-25 해지 (이중 로드 방지).

## 표준 (예약 — 트리거 도달 시 등재)

| 후보 | 트리거 |
| --- | --- |
| GOV.UK Service Manual | 다음 제품의 발견·조사 단계 착수 시 |
| Apple HIG / WCAG | 제품 UI 작업 재개 시 |

## 도구 (예약 — 트리거 도달 시 등재)

| 후보 | 트리거 |
| --- | --- |
| PostHog | 제품 출시로 실사용자 발생 시 (셀프호스트 유지비 주의) |
| Storybook · Playwright · axe-core | 웹 스택 제품 착수 시 |
