# Agent Handoff

## Context

- Date: 2026-07-29
- Repository: `/Users/miniminjae/.dotfiles`
- Branch: `main`
- User goal: iMac의 일반 대화형 판단 요청용 `agent-notify` 실험을 철회하고, 실행 요소는 롤백한 뒤 실패 기록만 남긴다.

## Current State

- `agent-notify decision` 실험은 실사용 알림이 도착하지 않아 실패로 판정하고 롤백했다.
- 제거 완료:
  - `agents/AGENTS.md`의 판단 질문 전 알림 호출 규칙
  - `bin/agent-notify`의 `decision` 명령
  - Codex execpolicy 정본과 `~/.codex/rules/agent-notify.rules` 심볼릭 링크
  - `install.sh`, `dotfiles-doctor`, 단위 테스트, README의 실험 연결
- 유지:
  - 기존 `~/.codex/hooks.json`, `~/.gemini/config/hooks.json` 정상 링크
  - 기존 완료·CLI 권한 요청 알림과 `agent-notify` sweep
  - D-016, D-017에 따른 기존 알림 자원 상한·회수 정책
- 실험 이벤트 파일의 `alerter_pid`는 모두 `null`이며, 프로세스 목록에도 `agent-notify`·`alerter`·알림용 `osascript`가 남아 있지 않았다. iMac의 메뉴 막대 LaunchAgent는 설치돼 있지 않다.
- sweep LaunchAgent는 매분 짧게 실행하고 종료하는 기존 작업이며 확인 시점 상태는 `not running`, 마지막 종료 코드는 0이었다.
- 커밋과 push는 하지 않았다.

## Decisions (cite, do not restate)

- 확정: `D-016`, `D-017` — 기존 `agent-notify` 자원 회수와 관제 정책.
- 철회: `일반 대화형 판단 요청용 agent-notify decision + Codex execpolicy` — 실사용 전달 실패와 불필요한 복잡성 때문에 D-번호로 승격하지 않고 제거했다.

## Files To Read First

- `/Users/miniminjae/.obsidian/mimir/40 Reviews/Runs/2026-07-29-agent-notify-decision-alert-rollback.md`
- `/Users/miniminjae/.obsidian/mimir/40 Reviews/Runs/2026-07-29-agent-notify-decision-approval-loop-fix.md`
- `agent-os/DECISIONS.md`의 D-016, D-017

## Work In Progress

- 저장소 실행 코드와 설정은 실험 전 상태로 복구됐다.
- 남은 저장소 변경은 문서뿐이다:
  - `README.md`: 이미 존재하는 Codex 훅 정본과 `PermissionRequest` 동작을 정확히 반영
  - `docs/conversation/handoff.md`: 실패·롤백 기록
- 저장소 밖에는 세 Run과 사용자 friction 기록이 남는다.

## Verification

- `agents/AGENTS.md`, `bin/agent-notify`, `bin/dotfiles-doctor`, `install.sh`, `tests/test_agent_notify.py`는 HEAD와 동일하다.
- `~/.codex/rules/agent-notify.rules`와 저장소의 `agents/codex/rules/`는 제거됐다.
- 실험 이벤트의 기록된 `alerter_pid`는 모두 `null`이다.
- `python3 -m unittest tests.test_agent_notify`: 54개 통과.
- `python3 -m py_compile bin/agent-notify`, `bash -n install.sh bin/dotfiles-doctor`, `git diff --check`: 통과.
- 프로세스 목록 확인: 조회 명령 자체 외 `agent-notify`·`alerter`·알림용 `osascript` 0개.

## Next Steps

- 이 실험을 자동 재개하지 않는다.
- 일반 대화형 판단 알림이 다시 필요해지면 새 요구와 자원 상한을 먼저 정의하고 별도 설계로 시작한다.

## Watch Outs

- 기존 CLI `PermissionRequest` 훅과 일반 대화형 판단 알림 실험을 혼동하지 않는다.
- 과거 두 Run의 구현 성공 문장은 당시 관찰 기록이며, 최종 판정은 이번 롤백 Run을 따른다.
- 기존 pending 이벤트나 알림 상태 파일은 사용자 데이터이므로 이번 롤백에서 삭제하지 않았다.
