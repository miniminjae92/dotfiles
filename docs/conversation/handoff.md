# Agent Handoff

## Context

- Date: 2026-07-21
- Repository: ~/.dotfiles (branch: main)
- User goal: 모델 중립 에이전트 환경 재설계 완료 후, 후속 개선 아이디어들의 실행

## Current State

- What is already done:
  - 재설계 5단계 + 용어 정리 + 가시성 3종 전부 완료·커밋 (bf3f678..984c3f8, 10커밋)
  - 공급자 중립 코어 `agents/AGENTS.md`(47줄, 상한 50), Codex/Gemini 심링크·Claude import
  - `agents/routing.json`: planner/worker/reviewer/clerk 역할, 부패 자원(윈도우)/저장 자원(주간 캡) 정책
  - 공유 스킬: work, developer-agent-os, handoff-session (`agents/skills/` → 양쪽 CLI 링크)
  - Claude 훅(Stop/Notification/PreCompact→agent-notify), 상태줄(ctx % 게이지), Brewfile, dotfiles-doctor
  - 아이디어 배치 평가 완료 → 결정은 developer-os 볼트 `10 Projects/시스템 개선 백로그.md`
- What is intentionally not changed:
  - `.codex/skills/`의 아카이브 체인(archive-session 등) — 감사 후 통합 예정
  - 알림 UX — 실불편 발생 전 백로그
  - 과거 DECISIONS(D-004 등)의 옛 용어 — 이력 보존 원칙, 현행 용어는 D-011
- Important assumptions:
  - agy(Antigravity 계열)가 `~/.gemini/GEMINI.md`를 읽는지 미검증
  - Claude 훅·상태줄은 다음 세션부터 발화/표시

## Key Decisions

- D-008 중립 코어 50줄 상한, D-009 구독 자원 라우팅, D-010 에스컬레이션=역할 재분류 로깅, D-011 용어 체계 (`agent-os/DECISIONS.md`)
- 아이디어 판정: 프롬프트 프록시 기각(코어 지시로 대체 완료), 아카이빙 감사 최우선, 우테코 콘텐츠 수집은 구조 안 기다리고 즉시, 트랙 2 저순위, 알림 UX 백로그

## Files To Read First

- `~/.obsidian/developer-os/10 Projects/시스템 개선 백로그.md`: 다음 세션들의 작업 지시서
- `agents/routing.json`: 역할·모델 라우팅 선언
- `agent-os/DECISIONS.md` D-008~D-011: 이번 재설계의 결정 원본

## Work In Progress

- Changed files: 없음 (워킹 트리 클린)
- Untracked files: 없음
- Known dirty state that should not be reverted: 커밋 10개가 로컬 전용 — push 여부 사용자 결정 대기 (iMac 동기화에 필요)

## Verification

- Command: `python3 -m unittest tests.test_agent_notify tests.test_personal_ops`
  Result: 통과 (33 + 7건, 2026-07-21)
- Command: `./bin/dotfiles-doctor`
  Result: 37 pass / 3 warn(ollama 미설치, magy·sagy 미로그인) / 0 fail

## Next Steps

1. (사용자) push 여부 결정 → iMac에서 pull + install.sh + brew bundle + dotfiles-doctor
2. 아카이빙 감사 — 새 세션, 플랜 모드, Opus. 기준: 재사용·보정·복구. Hermes 도입은 감사 후
3. 우테코 레벨3 학습 노트를 developer-os 00 Inbox에 수집 시작 (에이전트 불필요)
4. 트랙 2 (p10k/thefuck/nvm) — 새 세션, Sonnet, 착수 전 웹 재검증

## Watch Outs

- magy/sagy 첫 로그인 전이라 agy 계정 격리는 미가동 상태
- `/handoff-session` 등 새 스킬은 이 세션에는 안 보임 (세션 시작 후 링크됨) — 새 세션에서 확인
- 블로깅 분류축 세 번째(Learn/Build/?)를 사용자가 기억 못 함 — 백로그 노트에 채울 것
