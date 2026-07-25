# Agent Handoff

## Context

- Date: 2026-07-25
- Repository: ~/.dotfiles
- Branch: main (origin 동기화: `fe6a589..26d4251` push 완료)
- User goal: 에이전트 자산 구조 재편(grilling 방식 합의) + 매트 포컷 스킬 전량 벤더링 — **이번 세션에서 실행·검증까지 완료**. 다음 세션은 후속 관찰과 잔여 트랙.

## Current State

- 완료 (커밋 8건):
  - 구조 재편: 최상위 20+→13개. `agents/`=설비 세팅값(전부 홈 설치), `agent-os/`=운전 일지·계측 규격서(홈 링크 0). 공급자 어댑터 `agents/{claude,codex,gemini}/`, 어댑터 내부는 공급자 홈 미러
  - 매트 스킬 27종 신규 벤더(+기존 teach=active 28종), 스킬별 `VENDOR.md`. `mattpocock-skills` 플러그인은 **disable**(uninstall 아님 — `claude plugin enable`로 복귀 가능)
  - 문서: 루트 `CONTEXT.md`(용어 정본), README "Repository Layout" 절, D-014, `agent-os/upstreams.md`
  - 정리: scripts/ 해체(cleanclip→bin), test.md·은퇴 스크립트→yggdrasil 3-stash 보관 후 삭제, agy.old 154MB·docker-pb*·c_formatter_42 제거, nvim.log 삭제+ignore
- 의도적으로 안 한 것:
  - **다른 세션 WIP 2건 미커밋 보존**: `.config/nvim/assets/markdown-reader.css`, `docs/conversation/2026-07-23-neovim-markdown-reader-handoff.md` — 되돌리지 말 것
  - 아카이브 파이프라인 5종(`agents/codex/skills/`) 무수정 동결 — PostgreSQL 투영 구축 시 재설계(upstreams.md 명기)
  - doctor의 은퇴 launchd 검사(personal-ops-weekly WARN) 제거 — 다음에 doctor 손댈 때
- 가정: 벤더 스킬 완전 로드는 새 세션부터 (이번 세션 중 부분 로드는 실증됨, obsidian-vault 봉인 작동도 확인)

## Key Decisions

- Decision: 의미 규칙(agents=설비 세팅값/agent-os=운전 일지) + 홈 링크 0 불변식 + 2단 규약(결정→승격) + 축 A.
  Reason: 공급자는 부패 자원이라 기능 축+어댑터만 미래 변경(교체·신유형·중립화)을 흡수. 전문: `agent-os/DECISIONS.md` D-014.
- Decision: 벤더링은 단일 skills/ + 스킬별 VENDOR.md (frontmatter 기입·폴더 분리 금지), 갱신은 수동 diff.
  Reason: 스킬 파일을 upstream과 바이트 동일하게 유지해 갱신 diff를 깨끗하게. 수정 1건뿐: obsidian-vault 자동 발동 봉인(매트 볼트 규약 하드코딩).
- Decision: Codex 스킬 감사는 계측 트랙의 '자산 활용'(스킬 호출 분포) 측정 가동 후 데이터 기반으로.
  Reason: 측정 문법(질문→지표→결정)의 첫 실전 사례로 삼기 위해. 태스크 백로그 등록됨.

## Files To Read First

- `CONTEXT.md`: 이 레포 용어 정본 (설비 세팅값, 어댑터, 벤더링, 불변식…)
- `agent-os/DECISIONS.md`: D-014 (재검토 조건 포함)
- `agent-os/upstreams.md`: 벤더 현황·갱신법·재설계 예약
- `README.md` "Repository Layout" 절: 폴더→역할→설치 지도

## Work In Progress

- Changed files: 위 다른 세션 WIP 2건만 (이 세션 산출물 아님)
- Untracked files: 없음
- Known dirty state that should not be reverted: 그 2건

## Verification

- Command: `dotfiles-doctor`
  Result: 40 pass / 3 warn / 0 fail — D-014 불변식 검사 신설 후 첫 통과. warn 3은 기존 항목(ollama 선택 설치, personal-ops-weekly 은퇴 잔재, D-012 하드코딩 6파일)
- Command: `python3 -m unittest discover -s tests`
  Result: 123 tests OK (경로 갱신 후 — 갱신 전 test_lazygit_ai_commit 1건 실패했다가 수정)
- Command: `./install.sh` 재실행 + `find -L … -type l`(깨진 링크 탐색)
  Result: 링크 재생성 완료, 깨진 링크 0, Claude 스킬 36·Codex 42
- Command: `git push origin main`
  Result: `fe6a589..26d4251` 성공

## Next Steps

1. 새 Claude 세션에서 벤더 스킬 발동 확인 (`/grilling`, `/to-spec` 등). 이상 시 즉시 복귀: `claude plugin enable mattpocock-skills@mattpocock`
2. (원할 때) 벤더 갱신 실험: `github.com/mattpocock/skills` 받아 각 VENDOR.md 기준 diff → 선택 반영 → VENDOR.md 갱신
3. 계측 트랙 재개 시: `mimir/00 Inbox/agent-handoffs/2026-07-25-agentos-measurement.md`의 "다음 작업" 1번(Claude JSONL 실측)부터
4. doctor 손댈 때: personal-ops-weekly 은퇴 잡 검사 제거

## Watch Outs

- `agent-os/`에 홈으로 설치될 파일을 넣지 말 것 — 불변식 위반은 doctor가 FAIL로 잡음
- 벤더 스킬을 수정하면 반드시 해당 `VENDOR.md`에 수정 사실 기록 (선례: obsidian-vault)
- 행동 규칙 변경은 2단 규약 — DECISIONS.md 기록만 하고 agents/ 반영을 빼먹으면 미집행
- `~/.claude/plugins` 캐시의 매트 1.2.0은 disable 상태로 잔존 — 참조용, 지우지 않아도 됨
- 이전 핸드오프(2026-07-22: **imac SSH 미해결**, baby-monitor 배포 준비)는 이 파일의 git 이력에 보존 — imac SSH 복구됐는지 확인 필요
