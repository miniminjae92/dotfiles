# CLAUDE.md

@~/.dotfiles/agents/AGENTS.md

## Claude 전용

- 모델 라우팅의 단일 진실 공급원은 `~/.dotfiles/agents/routing.json`이다.
- 기본 모델은 Sonnet이다. 5시간 윈도우가 살아있는 동안 일상 구현도 Sonnet으로 수행한다.
- Opus(및 상위 모델)는 아키텍처 설계, 표준 시도 실패 후 디버깅, 보안·최종 리뷰에만 사용한다.
  주간 캡의 실질 지배 변수는 Opus 사용량이다.
- 윈도우·주간 캡이 소진되면 작업을 중단하지 말고 Codex(gcodex/ncodex)로 넘기라고 안내한다.
- 커밋 메시지·분류·요약 같은 기계적 작업은 기존 스크립트(`git ai-commit`, agy 경유)를 그대로 사용한다.
- 강결합 편집과 연속 설계 판단은 한 세션에서 유지하고, 독립적·경계가 명확한 작업만 서브에이전트에 위임한다.
