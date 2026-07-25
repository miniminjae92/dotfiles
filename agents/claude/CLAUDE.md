# CLAUDE.md

@~/.dotfiles/agents/AGENTS.md

## Claude 전용

- 모델 라우팅의 단일 진실 공급원은 `~/.dotfiles/agents/routing.json`이다.
- **Max 예외 기간(~2026-08-21): 기본 모델은 Opus다. 필요할 때 주저하지 않는다.** 기간 종료 시 이 절을 재검토해 갱신한다.
  산출물은 공급자 중립 자산(스킬·문서·코드)으로 남긴다.
- 윈도우·주간 캡이 소진되면 작업을 중단하지 말고 Codex(gcodex/ncodex)로 넘기라고 안내한다.
- 커밋 메시지·분류·요약 같은 정형 작업(clerk 역할)은 기존 스크립트(`git ai-commit`, agy 경유)를 그대로 사용한다.
- 강결합 편집과 연속 설계 판단은 한 세션에서 유지하고, 독립적·경계가 명확한 작업만 서브에이전트에 위임한다.

## 매트 포컷 스킬 시험 기간 (2026-07-24 ~ 재검토 전까지)

매트 포컷 스킬은 `~/.dotfiles/agents/skills/`에 **벤더링**해 주력으로 쓴다(active 전량, 스킬별 VENDOR.md, 플러그인 구독은 2026-07-25 해지 — D-014). 갱신은 upstream diff를 보고 수동 반영한다. 기능이 겹치면 매트 스킬을 우선한다:

- 세션 인계 → `/handoff` (`handoff-session` 대신. 단, Codex 등 타 CLI로 넘길 땐 기존 `handoff-session` 유지)
- 구현 워크플로 → `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement` (`$work` 대신. 단일 세션 규모면 grill 후 바로 `/implement`)
- 언어 공통화(UL 형성·합의·정착) → `domain-modeling`/`grill-with-docs`가 repo `CONTEXT.md` + `docs/adr/`에 기록. `term`은 즉석 의미 해명 전용으로 축소(2026-07-24 결정), 파일을 쓰지 않는다
- 새 repo에서 엔지니어링 플로우 첫 사용 전 `/setup-matt-pocock-skills` 1회 실행을 권한다.

기존 스킬(`handoff-session`, `work`, `term`)은 삭제하지 않고 보존한다. 시험 종료 시 이 절을 재검토해 통합 또는 원복한다.
