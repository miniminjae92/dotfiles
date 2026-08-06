# Scripts

`bin/` 스크립트 생태의 컨벤션과 레지스트리. 근거와 실험 조건은 DECISIONS.md D-012.

## 컨벤션

1. **언어**: 로직이 있으면 Python, 20줄 이하 순수 글루면 sh/bash. Ruby 신규 작성 금지(기존 것은 손댈 때 Python으로 이관 검토). 소급 재작성은 하지 않는다.
2. **경로**: vault 등 공유 경로는 하드코딩하지 않고 `agent-os/paths.env`에서 읽는다. 우선순위: 환경변수 > paths.env > 내장 기본값. 기본값으로 떨어지면 `ops-event`에 `reason=paths-contract-fallback`을 남긴다.
3. **관찰**: 백그라운드, 주기 잡은 실행 1건당 `ops-event` 1줄을 남긴다(ops-observability-spine 규약). 텔레메트리 실패가 잡을 깨뜨리면 안 된다.
4. **계층**: 모든 스크립트는 아래 셋 중 하나다. 계층이 요구 수준을 정한다.
   - **글루**: 래퍼, 단축. 테스트, 리팩터링 대상 아님. 죽으면 삭제.
   - **배관**: 훅, 수집, 주기 잡. 계약(스키마, 경로, 이벤트) 준수와 조용한 실패 처리가 핵심.
   - **제품**: 사실상 소프트웨어. 변경 빈도 × 실패 비용이 높으면 리팩터링, 테스트가 정당하다.
5. **레지스트리**: 스크립트를 추가, 삭제하면 아래 표를 갱신한다. `dotfiles-doctor`가 실물과의 diff를 감시한다.
6. **공유 라이브러리**: D-012 실험 통과 전에는 만들지 않는다.

## 레지스트리

| 이름 | 계층 | 목적 |
|---|---|---|
| `agent-os-capture-event` | 배관 | Stop 훅에서 세션 Run 이벤트 캡처 |
| `agent-os-core-check` | 배관 | SessionStart 훅: 공통 core drift 탐지 |
| `agent-os-friction` | 배관 | 생산성 불편일기에 마찰 항목 append |
| `agent-os-review-due` | 배관 | 리뷰 도래 여부 판정(JSON 출력) |
| `agent-os-tell-lint` | 배관 | 산출물/응답의 에이전트 티 규칙 린트 (warn: ops-event, enforce: block) |
| `agent-os-usage` | 배관 | 세션 로그 토큰 사용량 집계 |
| `agent-os-vault-snapshot` | 배관 | 볼트 git 스냅샷+푸시 (launchd) |
| `ai-model-status` | 제품 | 설정된 AI 모델 표시, 라이브 프로브 |
| `claude-statusline` | 배관 | Claude Code statusLine 렌더러 |
| `cleanclip` | 제품 | 클립보드 공백 정리 (tmux prefix+T) |
| `codex-session-export` | 배관 | codex 세션 jsonl → Markdown 내보내기 (은퇴 예정: D-019, `asx export` 구현 시 삭제) |
| `dotfiles-doctor` | 배관 | dotfiles, 에이전트 환경 read-only 헬스체크 |
| `git-cm-ai` | 글루 | lazygit-ai-commit exec 래퍼 |
| `harvest-sessions` | 배관 | 세션에서 사용자 발화 추출(수확 1단계) |
| `jobs-mcp` | 글루 | 키체인 인증키로 채용 MCP 서버(stdio) 기동 |
| `ko-style` | 배관 | 한국어 산출물 부호 규칙 검사, 수정(`--fix`) |
| `mirror-from-imac` | 배관 | 아이맥 → 맥북 역방향 미러(세션, 상태) |
| `mirror-to-imac` | 배관 | 맥북 → 아이맥 단방향 미러(수확 원천) |
| `notion-job` | 배관 | 노션 허브 정기 잡 실행(launchd, 수동 겸용) |
| `notion-mcp` | 글루 | 키체인 토큰으로 Notion MCP 서버(stdio) 기동 |
| `ops-digest` | 배관 | 이벤트 스트림 → 의사결정 다이제스트 |
| `ops-event` | 배관 | 백그라운드 잡 구조화 이벤트 수집 CLI |
| `personal-ops` | 제품 | 주간 리뷰, 보안 점검 자동화 (launchd) |
| `prfb` | 글루 | prfb-export 실행 래퍼 |
| `prfb-export` | 제품 | GitHub PR 피드백 → Obsidian 내보내기 |
| `prfbo` | 글루 | 내보낸 PR 피드백 fzf 선택 → nvim 열기 |
| `session-harvest` | 배관 | 세션 수확 파이프라인 2단계(마이닝+적재) |
| `vault-ai-classify` | 제품 | 볼트 노트 AI 분류 |
| `zcp` | 글루 | zoxide 질의 대상으로 cp |
| `zmv` | 글루 | zoxide 질의 대상으로 mv |
