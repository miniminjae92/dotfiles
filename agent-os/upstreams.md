# Upstreams: 외부 상류 대장

외부에서 들여오는 것들의 구독 현황판. 3분류(D-014):

- **워크플로**: 스킬로 벤더링해 들여온다 (수정 권리, 수동 diff 갱신)
- **표준**: 벤더링하지 않고 최신 원문을 참조한다 (확인일 관리)
- **도구**: 설치해서 피드백 시스템으로 쓴다

## 워크플로

| upstream | 방식 | 로컬 위치 | 상태 |
| --- | --- | --- | --- |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 벤더 (스킬별 VENDOR.md) | `agents/skills/`: active 29종 (2026-08-13 갱신, v1.2.3/84fdeff 기준) + upstream 삭제 2종 로컬 보존(edit-article, obsidian-vault) | 시험 기간 (CLAUDE.md 규약) |

- 갱신법: upstream 저장소를 받아 각 스킬의 VENDOR.md 기준 커밋/버전과 diff → 원하는 변경만 반영 → VENDOR.md의 commit과 날짜 갱신. `in-progress` 범주는 active가 아니므로 벤더링하지 않는다.
- 확인 주기: 정해 두지 않았다. 마지막 두 번의 확인이 2026-08-06 과 2026-08-13 이다. 주기를 정할지는 시험 기간 종료 시 함께 판단한다.
- 수정 현황: `obsidian-vault` 1건 (자동 발동 봉인, VENDOR.md에 사유 기록, upstream 삭제로 갱신 중단). 나머지 전부 무수정.
- 플러그인 구독은 2026-07-25 해지 (이중 로드 방지).

### 갱신 이력

- **2026-08-13, v1.2.2 → v1.2.3 (13커밋).** 차이가 있던 5종만 반영했다. `diagnosing-bugs`
  에 `## Redact` 절이 추가됐다(명령, 출력, 캡처 산출물의 시크릿을 `<REDACTED>` 로 치환하고,
  마스킹한 출력으로 진단이 안 되면 사용자에게 묻는다). `wizard` 는 `TOTAL_MINUTES` 와 남은
  시간 표시를 없애고 단계 수로 대체했다. `code-review`, `codebase-design`,
  `improve-codebase-architecture` 는 서브에이전트 호출 지시에서 Claude Code 고유 표현
  (`Agent` 도구, `subagent_type=Explore`)을 걷어내 하네스 중립으로 바꿨다. 마지막 셋은
  AGENTS.md 의 공급자 중립 원칙과 같은 방향이라 그대로 받았다.
- 2026-08-06, v1.2.2 반영. 신규 wizard, to-questionnaire, wait-what.
  writing-great-skills 를 writing-for-agents 로 rename.

## 표준 (예약: 트리거 도달 시 등재)

| 후보 | 트리거 |
| --- | --- |
| GOV.UK Service Manual | 다음 제품의 발견, 조사 단계 착수 시 |
| Apple HIG / WCAG | 제품 UI 작업 재개 시 |

## 도구 (예약: 트리거 도달 시 등재)

| 후보 | 트리거 |
| --- | --- |
| PostHog | 제품 출시로 실사용자 발생 시 (셀프호스트 유지비 주의) |
| Storybook/Playwright/axe-core | 웹 스택 제품 착수 시 |
