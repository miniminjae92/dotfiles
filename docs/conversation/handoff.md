# Agent Handoff

## Context

- Date: 2026-08-04 (밤)
- Repository: `/Users/miniminjae/.dotfiles` 중심. 파생 작업이 닿은 곳: 신규 추출 레포 4개(`~/projects/{mdview,kman,video-summary,git-ai-commit}`), `~/projects/{dref,naon,manual-library,gh-mine}`, mimir vault, iMac(ssh `imac`)
- Branch: dotfiles `main`. dref만 `feat/ux-proposal-adoption`
- User goal: ① 매일 보안점검 감사 ② 루틴 전수 검수·개선(P0~P2) ③ dotfiles의 실질 도구를 포트폴리오용 독립 레포로 추출(Wave 0~4)

## Current State

- 완료(전부 오늘): 감사 종합 보고 → P0 신호 복원(D-020) → P1 자원·가시성(D-021) → P2 위생(D-021 개정) → Wave 0(README 3건+포트폴리오 등재 계획) → Wave 1(mdview·kman 추출, D-022) → Wave 2(video-summary·git-ai-commit 스위트 추출, D-022 개정) → 주간 수확을 일→**목 20:30**으로 이동
- 전체 지도는 mimir 계획 문서(아래) — 각 항목에 실행 결과·커밋 해시가 체크돼 있다
- 의도적으로 안 한 것:
  - dref 서버 재시작 안 함 — 작업트리에 사용자 개편 WIP(ux.js 등)가 있어 재시작하면 미완성 코드가 활성화됨. P2의 dref 코드 수정은 다음 자연 재시작부터 적용
  - iMac에 추출 레포 clone 안 함(규약: 필요할 때만) — iMac의 `~/.local/bin/{kman,mdview,video-summary,git-ai-commit,git-plan-ai,lazygit-ai-commit}` 심링크는 dangling. iMac 자동화는 이 도구들을 안 쓰므로 무해. **예외: agent-notify는 iMac이 실가동(sweep·menu)하므로 Wave 3에서 rsync로 배치·전환 완료** — push 후 origin 지정만 하면 됨
  - `tests/test_asx.py` 기존 실패 1건 미수리(이 작업과 무관 — asx의 mirror 지원 확장 때 테스트 미갱신, 별건)
  - gitleaks 시크릿 스캔은 D-020에서 보류 — 레포 공개 절차의 게이트로 편입 예정
- 가정: 수확·agentos-monitor의 정본 가동처는 iMac (오늘 라이브 확인함)

## Decisions (cite, do not restate)

- 확정: `D-020` — 보안점검·다이제스트 신호 복원 (상태: 파일럿, 재검토 조건 있음)
- 확정: `D-021` — 백그라운드 자원 회수·계측 위생 (+개정: P2 집행)
- 확정: `D-022` — 도구 추출, dotfiles는 소비자 (+개정: Wave 2 집행)
- 미결: session-harvest 존폐 — ⓐ 수리 적용됨, **킬 기준: 목요일(08-06, 08-13) 2회 연속 스텁이면 공식 중단**. 실패는 digest 오류 섹션에 뜬다
- 미결: `~/projects/claude-code`(유출 스냅샷 미러) public 유지 여부 — 포트폴리오 제외는 합의, 비공개 전환은 사용자 판단 대기
- 미결: 포트폴리오 MDX 작성 — 스키마의 problem·judgment·metrics는 본인 몫(계획 문서에 엔트리별 표 있음)
- 확정: `D-022` 개정 — Wave 3(agent-notify+menu) 집행 완료(2026-08-04 밤, 후속 세션). launchd 2종 무중단 전환, 양 기기 doctor 0 fail
- 미결: Wave 4(asx·codex-accounts·simulator-reaper·prfb) 실행 여부·시점

## Files To Read First

- `~/.obsidian/mimir/00 Inbox/dotfiles 감사·독립 레포 계획 2026-08-04.md`: 오늘 전체의 지도 — 감사 근거, P0~P2 체크 결과, Wave별 상태, 포트폴리오 등재 계획표
- `agent-os/DECISIONS.md` D-020~D-022: 행동이 바뀐 부분의 정본
- `git log fa89686..59faa95`: dotfiles 쪽 변경 6커밋의 요약

## Work In Progress

- Changed files: 없음 — dotfiles 작업트리 클린
- **push 대기**: dotfiles `main`이 origin보다 11커밋 앞섬(`b359f45`부터 HEAD까지, Wave 3 포함 — `git log origin/main..` 실측). 신규 레포 5개는 커밋 완료·원격 미생성:
  ```bash
  gh repo create miniminjae92/mdview        --public --source ~/projects/mdview        --push
  gh repo create miniminjae92/kman          --public --source ~/projects/kman          --push
  gh repo create miniminjae92/video-summary --public --source ~/projects/video-summary --push
  gh repo create miniminjae92/git-ai-commit --public --source ~/projects/git-ai-commit --push
  gh repo create miniminjae92/agent-notify  --public --source ~/projects/agent-notify  --push
  ```
- 다른 레포 커밋(각자 push 대기): dref `4468dcb`·`d0c0619`(개편 브랜치 위), naon `cf00c17`, manual-library `33d0ddc`, gh-mine `da0f0fa`
- iMac dotfiles: 같은 커밋들을 `git am`으로 적용해 둠 — 맥북 push 후 iMac pull 시 동일 내용이라 충돌 없이 정리됨
- Known dirty state that should not be reverted: dref(`ops/install.sh`, `src/domain/ux.js`, `src/web/public/projects.js` + untracked library items), naon(문서 5개), manual-library(3개) — 전부 **사용자 WIP**, 건드리지 말 것

## Verification

- Command: `python3 -m unittest discover -s tests` (dotfiles)
  Result: 104개 중 103 통과 — 유일 실패는 기존 `test_asx.py` 1건(별건)
- Command: `~/.dotfiles/bin/dotfiles-doctor`
  Result: 48 pass · 1 warn(D-012 설계상 baseline) · **0 fail**
- 신규 레포 테스트: mdview 6 · kman 12 · video-summary 29 · git-ai-commit 16 — 전부 OK
- 라이브 확인: `git ai-commit help`·`man -w git-ai-commit`·`video-summary --help` 새 심링크로 정상. 21:00 digest가 `mimir/40 Reviews/백그라운드 잡 다이제스트 minjaes-MacBook-Pro.md`에 착지({host} 분리 작동). 보안점검 활성 이상 3건 전부 진짜(backup-missing·방치 http.server·macos-updates)

## Next Steps

1. (사용자) push: dotfiles 6커밋 + 위 `gh repo create` 4건 + naon/manual-library/gh-mine
2. ~~Wave 3~~ ✅ 완료(2026-08-04 밤 후속 세션) — `~/projects/agent-notify`, 양 기기 전환·검증 끝. push만 남음
3. Wave 4: asx·codex-accounts(usage+래퍼 4종)·simulator-reaper·prfb
4. 목 08-06 20:30 이후: 수확 결과 확인 — 스텁이면 1회차 실패 기록(digest에 뜸)
5. 포트폴리오 MDX 초안(설명보따리부터) — 계획 문서의 표 참조, 본인 목소리로

## Watch Outs

- `.zshrc`의 `MANPATH`·`VIDEO_SUMMARY_DIR` export는 **새 셸부터** 적용
- battery는 제3자 plist — `battery` CLI로 maintain 재설정하면 stdout 로그 차단이 되돌아갈 수 있음(D-021 개정에 기록)
- 방치된 `python -m http.server 8899`(다른 세션 잔재, PID 51865)가 아직 살아 있으면 `kill 51865` — 보안점검 활성 목록에서 확인 가능
- iMac에서 install.sh 재실행 시 추출 도구 6개의 `skip: … (클론 없음)` 출력은 정상 동작
- 추출 레포의 CI는 GitHub push 후에야 처음 돈다 — ubuntu 러너에서 깨지면(특히 kman의 pager/man 관련) 그때 수정
- dref-harvest의 50분 행(hang) 3건은 severity만 고쳤고 원인 미진단 — 재발하면 digest 오류 섹션에 message로 보인다
