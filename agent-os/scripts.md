# Scripts

`bin/` 스크립트 생태의 컨벤션과 레지스트리. 근거와 실험 조건은 DECISIONS.md D-012.

## 컨벤션

1. **언어**: 로직이 있으면 Python, 20줄 이하 순수 글루면 sh/bash. Ruby 신규 작성 금지(기존 것은 손댈 때 Python으로 이관 검토). 소급 재작성은 하지 않는다.
2. **경로**: vault 등 공유 경로는 하드코딩하지 않고 `agent-os/paths.env`에서 읽는다. 우선순위: 환경변수 > paths.env > 내장 기본값. 기본값으로 떨어지면 `ops-event`에 `reason=paths-contract-fallback`을 남긴다.
3. **관찰**: 백그라운드·주기 잡은 실행 1건당 `ops-event` 1줄을 남긴다(ops-observability-spine 규약). 텔레메트리 실패가 잡을 깨뜨리면 안 된다.
4. **계층**: 모든 스크립트는 아래 셋 중 하나다. 계층이 요구 수준을 정한다.
   - **글루**: 래퍼·단축. 테스트·리팩터링 대상 아님. 죽으면 삭제.
   - **배관**: 훅·수집·주기 잡. 계약(스키마·경로·이벤트) 준수와 조용한 실패 처리가 핵심.
   - **제품**: 사실상 소프트웨어. 변경 빈도 × 실패 비용이 높으면 리팩터링·테스트가 정당하다.
5. **레지스트리**: 스크립트를 추가·삭제하면 아래 표를 갱신한다. `dotfiles-doctor`가 실물과의 diff를 감시한다.
6. **공유 라이브러리**: D-012 실험 통과 전에는 만들지 않는다.

## 레지스트리

| 이름 | 계층 | 목적 |
|---|---|---|
| `agent-notify` | 제품 | 에이전트 CLI 공용 영속 알림(배너·알림 스위프) |
| `agent-os-capture-event` | 배관 | Stop 훅에서 세션 Run 이벤트 캡처 |
| `agent-os-core-check` | 배관 | SessionStart 훅: 공통 core drift 탐지 |
| `agent-os-friction` | 배관 | 생산성 불편일기에 마찰 항목 append |
| `agent-os-review-due` | 배관 | 리뷰 도래 여부 판정(JSON 출력) |
| `agent-os-usage` | 배관 | 세션 로그 토큰 사용량 집계 |
| `agent-os-vault-snapshot` | 배관 | 볼트 git 스냅샷+푸시 (launchd) |
| `ai-model-status` | 제품 | 설정된 AI 모델 표시·라이브 프로브 |
| `asx` | 제품 | 에이전트 세션 통합 탐색기(search/list/show) |
| `claude-statusline` | 배관 | Claude Code statusLine 렌더러 |
| `codex-account` | 글루 | codex 계정 프로필 선택 실행 래퍼 |
| `codex-account-login` | 글루 | codex 계정 로그인 헬퍼 |
| `codex-account-usage` | 제품 | codex 계정별 사용량 조회 (launchd) |
| `codex-session-export` | 배관 | codex 세션 jsonl → Markdown 내보내기 |
| `dotfiles-doctor` | 배관 | dotfiles·에이전트 환경 read-only 헬스체크 |
| `gcodex` | 글루 | google 계정 codex 래퍼 |
| `git-ai-commit` | 제품 | AI 커밋 계획 수립·검증·적용 |
| `git-cm-ai` | 글루 | lazygit-ai-commit exec 래퍼 |
| `git-plan-ai` | 제품 | 읽기 전용 AI 커밋 플랜 생성 |
| `harvest-sessions` | 배관 | 세션에서 사용자 발화 추출(수확 1단계) |
| `kman` | 제품 | man 페이지 한국어 번역(캐시+용어집) |
| `lazygit-ai-commit` | 제품 | lazygit용 AI 커밋 통합 |
| `magy` | 글루 | main 계정 agy 래퍼 |
| `ncodex` | 글루 | naver 계정 codex 래퍼 |
| `ops-digest` | 배관 | 이벤트 스트림 → 의사결정 다이제스트 |
| `ops-event` | 배관 | 백그라운드 잡 구조화 이벤트 수집 CLI |
| `personal-ops` | 제품 | 주간 리뷰·보안 점검 자동화 (launchd) |
| `prfb` | 글루 | prfb-export 실행 래퍼 |
| `prfb-export` | 제품 | GitHub PR 피드백 → Obsidian 내보내기 |
| `prfbo` | 글루 | 내보낸 PR 피드백 fzf 선택 → nvim 열기 |
| `sagy` | 글루 | sub 계정 agy 래퍼 |
| `session-harvest` | 배관 | 세션 수확 파이프라인 2단계(마이닝+적재) |
| `vault-ai-classify` | 제품 | 볼트 노트 AI 분류 |
| `video-summary` | 제품 | YouTube 타임스탬프 요약 → Markdown 노트 |
| `zcp` | 글루 | zoxide 질의 대상으로 cp |
| `zmv` | 글루 | zoxide 질의 대상으로 mv |
