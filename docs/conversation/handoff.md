# Agent Handoff

직전 핸드오프(감사·P0~P2·Wave 0~2)는 `69ac3b0`에 남아 있다.
이 노트는 2026-08-04 밤 후속 세션(Wave 3·4 + 전체 push)까지 반영한 최종본이다.

## Context

- Date: 2026-08-05 (04 밤 세션 종료 시점)
- Repository: `/Users/miniminjae/.dotfiles` 중심. 파생: 추출 레포 8개(`~/projects/{mdview,kman,video-summary,git-ai-commit,agent-notify,asx,codex-accounts,simulator-reaper}`), `~/projects/{naon,manual-library,gh-mine,dref}`, mimir vault, iMac(ssh `imac`)
- Branch: dotfiles `main` — **origin과 완전 동기, 워킹트리 클린**
- User goal: 하루 아크 = ① 보안점검 감사 ② 루틴 개선(P0~P2) ③ 실질 도구의 포트폴리오용 독립 레포 추출(Wave 0~4). **추출 시리즈는 이 세션으로 종료됨**

## Current State

- 완료: 감사 → P0(D-020) → P1·P2(D-021) → Wave 0(README 3건) → Wave 1(mdview·kman) → Wave 2(video-summary·git-ai-commit) → **Wave 3(agent-notify+메뉴 앱) → Wave 4(asx·codex-accounts·simulator-reaper)** → **전체 push**(사용자 지시)
- 공개 레포 8개 전부 히스토리 보존·MIT·README·**CI 그린**: <https://github.com/miniminjae92/>{mdview,kman,video-summary,git-ai-commit,agent-notify,asx,codex-accounts,simulator-reaper}
- dotfiles는 소비자: bin 39→**25**, install.sh가 `~/projects/<repo>` 클론 존재 시 링크(없으면 skip). launchd 잡 4종(agent-notify-sweep·menu·codex-account-usage·simulator-reaper)은 심링크 재지정만으로 무중단 전환됨
- 다른 레포 push도 완료: naon(이미 동기였음)·manual-library(10커밋)·gh-mine(1커밋)·dref(`feat/ux-proposal-adoption` 신규 원격 브랜치, 15커밋)
- iMac: dotfiles 동일 해시 동기(`56fe72d`), 추출 레포 중 실가동 4개(agent-notify·asx·codex-accounts·simulator-reaper) rsync 배치·origin 연결·upstream 설정 완료. 나머지 4개는 미배치(규약: 필요할 때만)
- 의도적으로 안 한 것:
  - **prfb 추출 안 함** — 근거 미달(테스트 0 + 소비 증거 미확인). 사유·재검토 조건은 D-022 개정에 명기
  - dref 서버 재시작 안 함(사용자 개편 WIP 활성화 위험 — 이전 세션과 동일 사유)
  - miniminjae.me는 손대지 않음 — 별도 터미널의 라이브 세션이 카테고리별 페이지 디자인 진행 중이었음
  - `agent-notify mode`가 `local=off slack=off`(전체 무음)인 것은 사용자 상태로 판단해 보존 — 테스트 격리 검증으로 이 세션이 만든 게 아님을 확인함. 의도 아니면 `agent-notify mode normal`

## Decisions (cite, do not restate)

- 확정: `D-020` — 보안점검·다이제스트 신호 복원 (파일럿)
- 확정: `D-021` — 백그라운드 자원 회수·계측 위생 (+개정: P2)
- 확정: `D-022` — 도구 추출, dotfiles는 소비자 (+개정 3건: Wave 2 / Wave 3 / **Wave 4 — prfb 잔류 판정 포함**)
- 미결: session-harvest 존폐 — **킬 기준: 목요일(08-06, 08-13) 2회 연속 스텁이면 공식 중단**. 실패는 digest 오류 섹션에 뜬다
- 미결: `~/projects/claude-code`(유출 스냅샷 미러) public 유지 여부 — 포트폴리오 제외는 합의됨
- 미결: 포트폴리오 MDX 작성 — problem·judgment·metrics는 본인 몫 (mimir 계획 문서에 엔트리별 표)

## Files To Read First

- `~/.obsidian/mimir/00 Inbox/dotfiles 감사·독립 레포 계획 2026-08-04.md`: 하루 전체의 지도 — Wave 0~4 전부 ✅ 체크된 상태
- `agent-os/DECISIONS.md` D-020~D-022: 정본. D-022 개정 3건에 각 Wave의 방법·판정이 있다
- `install.sh`: 추출 도구 링크 목록(external_tool)과 메뉴 앱 빌드(클론 소스) — 새 기기 셋업 시 동작 기준

## Work In Progress

- Changed files: 없음 — dotfiles·추출 레포 8개 전부 클린, origin 동기
- Untracked files: 없음
- Known dirty state that should not be reverted:
  - dref(`ops/install.sh`, `src/domain/ux.js`, `src/web/public/projects.js` + untracked library items), naon(문서 5개), manual-library(3개) — 전부 **사용자 WIP**
  - iMac `.config/nvim/lazy-lock.json` 로컬 수정 — 그 기기 플러그인 상태, 커밋·리셋 금지

## Verification

- Command: `python3 -m unittest discover -s tests` (dotfiles, 양 기기)
  Result: **33/33 전부 통과** — 기존 test_asx 실패는 asx 레포로 이관하며 수리됨(오늘 처음 완전 그린)
- Command: `dotfiles-doctor` (양 기기)
  Result: 48 pass · 1 warn(D-012 설계상 baseline) · 0 fail
- 추출 레포 테스트: agent-notify 56 · asx 2 · codex-accounts 13 · simulator-reaper 12(신설) — 전부 OK
- CI: 8레포 전부 성공. codex-accounts는 ubuntu 러너에서 1회 실패(로그인 플로우가 macOS 전용) 후 **macOS 러너로 교체해 그린**(`2b0e7c8`)
- 라이브: 심링크 7종 재지정 확인, launchd 4종 exit 0, `AgentNotifyMenu --check` OK(양 기기), `asx list` 정상

## Next Steps

1. 포트폴리오 MDX 초안(설명보따리부터) — 계획 문서의 표 참조, 본인 목소리로. 추출 8레포도 등재 후보(judgment 원천은 각 D-번호·README)
2. 목 08-06 20:30 이후: 수확 결과 확인 — 스텁이면 1회차 실패 기록
3. `~/projects/claude-code` 공개 여부 판단(사용자)
4. 필요 시 iMac에 나머지 추출 레포 4개 clone(규약: 필요할 때만)

## Watch Outs

- 추출 레포를 고칠 땐 **레포에서 고치고 push** — dotfiles bin에는 이제 코드가 없다. 양 기기 반영은 각 레포 pull
- codex-accounts CI는 macOS 러너(느림·큐 대기 있음) — ubuntu로 되돌리면 로그인 테스트가 다시 깨진다
- iMac ssh 비로그인 셸은 homebrew PATH가 없어 doctor가 가짜 "tool missing" 15 fail을 낸다 — `PATH="/opt/homebrew/bin:...:$PATH"` 붙여 실행하면 0 fail
- battery는 제3자 plist — `battery` CLI로 maintain 재설정하면 stdout 로그 차단이 되돌아갈 수 있음(D-021 개정)
- dref-harvest 50분 행(hang) 원인 미진단 — 재발하면 digest 오류 섹션에 뜬다
- `.zshrc` env(MANPATH·VIDEO_SUMMARY_DIR)는 새 셸부터 적용
