# Agent Handoff

## Context

- Date: 2026-07-22
- Repository: ~/.dotfiles (home base) + ~/projects/my/baby-monitor + ~/projects/my/audio-workbench
- Branch: main (all)
- User goal: 여러 갈래 세션 — (1) imac SSH 양방향, (2) 볼트 스왑·폰 열람 자동화, (3) baby-monitor 배포 준비·음원/BM 전략. 지금 활성 초점은 **baby-monitor 배포 준비**, 미해결은 **imac SSH**.

## Current State

- 완료:
  - 볼트 스왑(mimir↔yggdrasil) + GitHub·Obsidian·dotfiles 참조 동기화, 커밋·push (036efb0)
  - 볼트 매시간 원격 push 자동화(폰 열람용), launchd 실환경 검증 통과 (e23f924)
  - baby-monitor 손실방지: 비공개 원격 생성 + 8커밋 push (권리 미확인 루트 m4a는 .gitignore로 이력 차단)
  - 음원 제작 워크벤치를 audio-workbench repo(비공개)로 분리, baby-monitor에서 제거 (34417c7)
- 의도적으로 안 한 것:
  - baby-monitor 배포 준비물(Info.plist·아이콘·개인정보처리방침 등) — cowork 세션에 위임 예정(아래 프롬프트)
  - 사업자등록 — 지금 안 함(수익화가 트리거)
  - dotfiles 워킹트리의 Brewfile·bin/claude-statusline·claude/CLAUDE.md — **사용자 본인 WIP, 건드리지 말 것**
- 미해결(중요): **imac SSH 접속 불가** — 아래 Watch Outs 참조

## Key Decisions

- BM: 무료 출시 → 프리미엄 기능을 **소액 일회성 비소모성 IAP 언락**으로. **광고 안 함**(베이비 모니터엔 유해). 프라이버시(로컬 P2P, 영상 기기 밖 안 나감)가 차별점이자 유료 정당성.
  Reason: 첫 앱·검증·포트폴리오 단계 → 무료로 도달 극대화, 소액 구매는 프리미엄에 얹어 기존 사용자 안 잃고 수익화.
- 사업자등록: 지금 안 함. 사용자는 피부양자 아님(지역가입자)이라 "피부양자 상실" 함정은 무관 → 미리 등록은 무해하나 실익도 작음. 수익화 시 간이과세자.
  Reason: 무료 단계엔 등록 의무 없음(Apple은 유료/IAP=Paid Agreement 체결 시 BRN 요구). 와이프 명의는 주부라 이점 없음.
- Apple 등록: **Individual**(D-U-N-S 불필요, 연 ₩129,000). 판매자명=실명이나 앱 표시명은 "잘자라 우리아기"로 별개.
- 음원(baby-monitor D-016): 자장가=사용자 제공(임포트·부모 목소리 녹음) 중심 + PD곡·CC0 프리셋 소수 번들. 백색소음=앱 런타임 합성. **YouTube 추출·임베드 재생 경로는 기각**(소유해도 ToS·광고·오프라인·의존성 문제).
- 앱 이름 방향: "잘자라 우리아기"(KR) + 기능 부제("베이비 모니터·홈캠"). 글로벌은 별도 영문 브랜드.

## Files To Read First

- `~/projects/my/baby-monitor/DECISIONS.md`: D-001~D-017(예정). 특히 D-016(음원), D-014(출시 게이트)
- `~/.obsidian/mimir/00 Inbox/reports-2026-07-22/deploy-research.md`: App Store 첫 배포 체크리스트·심사 리스크(§2)·준비물(§4)
- `~/.obsidian/mimir/00 Inbox/아침 브리핑 2026-07-22.md`: 밤샘 감사 13건 통합(baby-monitor 원격 push=§2 최상단 ①, 완료)

## Work In Progress

- Changed files (dotfiles): Brewfile, bin/claude-statusline, claude/CLAUDE.md — **사용자 본인 작업, 유지**
- Untracked: 없음
- baby-monitor / audio-workbench: 워킹트리 클린, 원격 동기화됨
- Known dirty state: 위 dotfiles 3개는 되돌리지 말 것

## Verification

- Command: `python3 -m unittest tests.test_personal_ops tests.test_agent_notify` (dotfiles)
  Result: 40 tests, OK (2026-07-22)
- Command: `./bin/dotfiles-doctor`
  Result: 37 pass / 3 warn / 0 fail
- Command: launchctl kickstart 볼트 스냅샷 잡 + push --dry-run
  Result: 두 볼트 원격 동기화 ✓, 에러 로그 0
- baby-monitor Swift 테스트: **이번 세션 미실행**(문서·config 변경만) — cowork에서 변경 후 실행 필요

## Next Steps

1. (사용자, 최우선) imac SSH 복구 — imac에서 `ssh localhost 'echo ok'` + `ssh 100.123.120.70 'echo ok'`로 sshd vs tailscale 갈래 확정 → tailscale이면 **메뉴바 Tailscale 앱 Quit→재실행**(down/up으론 부족했음). 이후 macbook에서 `ssh imac` 재확인.
2. (cowork 세션, baby-monitor repo) 배포 병렬 준비물:
   - D-017 신설(위 Key Decisions: BM·사업자등록·Apple 유형·음원)
   - Config/BabyMonitor-Info.plist에 `ITSAppUsesNonExemptEncryption = NO`
   - Assets.xcassets/AppIcon.appiconset 스캐폴드(1024 placeholder) + project.yml 반영
   - D-014 게이트: 릴리스 아카이브에 미허가 음원(LocalAssets/Audio·루트 m4a) 미포함 확인
   - docs/legal/PRIVACY.md·SUPPORT.md 초안(한/영, "수집 없음·로컬 P2P")
3. (사용자) Apple Developer 등록(Individual, ₩129,000) 시작 여부 — 승인 수 주 걸리는 임계 경로. 본인+와이프 테스트는 무료 Personal Team으로 병행 가능, 지인 TestFlight은 등록 후.
4. (사용자) 앱 아이콘 1024×1024 원본, 앱 표시명 중복 검색.

## Watch Outs

- **imac SSH**: `ssh imac`/`100.123.120.70:22` → kex reset 지속. macbook RunSSH=false, tailnet 데이터경로는 정상(pong 78ms), LAN 192.168.35.5는 no route. 원인 유력: App Store 샌드박스 tailscaled가 tainet 22를 스테일 점유. `--ssh=false` + down/up으로 안 풀림 → 앱 재시작 필요. imac 접근은 VNC(`vnc://minjaes-imac`)로 가능.
- Tailscale는 App Store 샌드박스 빌드라 **Tailscale SSH 서버 못 돌림**. B(Tailscale SSH) 쓰려면 standalone tailscaled 필요 — 비추. A(Remote Login+키, Tailscale 터널 위)가 본체.
- baby-monitor: 권리 미확인 루트 m4a(바스락·브람스자장가·진공청소기) git 이력에 넣지 말 것. 2.1G 오디오는 의도적 git 제외(로컬 전용, PD/CC0로 대체 예정).
- `.venv-audio`(baby-monitor 루트)는 이번에 삭제함(워크벤치 이관으로 고아) — 재생성은 audio-workbench의 bootstrap.sh.
- 폰 열람: `github.com/miniminjae92/{yggdrasil,mimir}` 로그인(웹/앱). 공개 Pages 아님(사용자가 비공개 선택).
