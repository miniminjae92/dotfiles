# Agent Handoff

직전 핸드오프(Wave 3, Wave 4 집행과 전체 push)는 `c4b51c9`에 남아 있습니다.
이 노트는 2026-08-06 하루에 병행된 Claude 세션 다섯 갈래를 합친 것입니다. 사용자 지시로
흩어진 글쓰기 규칙을 한 곳에 모으고 중복을 정리한 결과까지 반영했고, 이후 갈래 5(Ghostty
reader-dark 테마)가 추가됐습니다.

## Context

- Date: 2026-08-06
- Repository: `/Users/miniminjae/.dotfiles`(주), `/Users/miniminjae/projects/ww-req/delivery-discount/*`(대행), mimir vault
- Branch: dotfiles `main`, 워킹트리 더러움
- User goal: 네 갈래가 한 질문으로 수렴합니다. "에이전트가 쓰는 글의 규율을 모호한 지시가 아니라 검사 가능한 기준으로 만들 수 있는가"

## Current State

### 갈래 1: nn98/delivery-discount-api 대행 (외부, 리뷰 대기)

- PR https://github.com/nn98/delivery-discount-api/pull/1 열림. `MERGEABLE / CLEAN`, 커밋 1개, 리뷰 0
- 기능: 종료일이 지난 할인을 `/api/brands` 응답에서 제외합니다. 구간(`DiscountTier`) 단위 판정, 요청 시점 계산, `Asia/Seoul` 고정, 종료일 당일까지 유효
- 응답 스키마, `export.json` 스키마, tracker 판독 규칙 모두 무변경입니다. web도 무변경으로 동작합니다
- 테스트 75건 전원 통과(신규 15건). 리베이스 2회로 오너 커밋 4개를 흡수했습니다

### 갈래 2: 커밋, PR, 이슈 말투 규약 (dotfiles, `31b8767`로 커밋됨)

- `agents/AGENTS.md:10`이 "the configured commit-message convention"을 쓰라면서 경로를 안 알려주는 실행 불가능한 지시였습니다. 두 정본을 가리키도록 교체했고 50줄 캡(D-008)은 유지했습니다
- `agents/conventions/commit-message/korean-angularjs.md`를 35줄에서 약 120줄로 확장했습니다. 축별 정본 분담표, 3계층 우선순위표, 대상 저장소 측정 절차, 산출물별 말투표를 넣었습니다
- GitHub 실물 정리: PR 제목과 커밋 제목을 서술형에서 명사형으로 수정, `miniminjae92/naon` 이슈 6건 제목을 명사형으로 변경했습니다(본문은 유지)

### 갈래 3: 티 집행 배관 (다른 세션, 미커밋)

- `agents/tell-rules.tsv`, `bin/agent-os-tell-lint`, `bin/ko-style` 신규(전부 untracked)
- 라이브 `~/.claude/settings.json`과 정본 `agents/claude/settings-fragment.json` 양쪽에 배선됐고 심링크도 생성됐습니다
- 정본 문서는 `~/.obsidian/mimir/20 Knowledge/좋은 글 작성 기준.md`이고, 별도 인계 노트가 `~/.obsidian/mimir/00 Inbox/agent-handoffs/2026-08-06-좋은-글-작성-기준-인계.md`에 있습니다

### 갈래 4: 매트 포컷 스킬 upstream 동기화 (다른 세션, 미커밋)

- v1.2.0에서 v1.2.2(`8b36d4f`)로 갱신, active 28종에서 29종
- 신규 3종: `wizard`, `to-questionnaire`, `wait-what`
- 이름 변경: `writing-great-skills`에서 `writing-for-agents`로. 잔존 참조 없고 `~/.claude/skills` 심링크도 정상입니다
- upstream 삭제 2종은 로컬 보존: `edit-article`, `obsidian-vault`
- `agent-os/upstreams.md` 갱신됨

### 갈래 5: Ghostty reader-dark 테마 (이 세션, 커밋 완료 `0a2ff9f`, `0ba7325`)

- 목표: iTerm2 무영향, 디자인 터미널별 독립, 기능 공유를 지키면서 `leader+mp`/mdview의
  리더 다크 스타일로 Ghostty, nvim, fzf, bat, Starship, lualine을 통일
- 팔레트 정본은 `.config/nvim/assets/markdown-reader.css`의 `[data-theme="dark"]` 블록.
  정본에 없는 빨강은 테라코타 `#d47f77`, 브라이트블랙은 `#707a7d`로 파생(근거는 커밋 본문)
- `.zshrc`에 `_is_ghostty` 헬퍼 신설(`TERM_PROGRAM` 또는 `GHOSTTY_RESOURCES_DIR`).
  의도된 동작 변화: Ghostty에서 띄운 tmux 세션이 이제 p10k가 아니라 Starship을 받습니다
- nvim은 `colors/reader-dark.lua`(수제 스킴, 약 130개 그룹)와 `core/term.lua`로
  Ghostty에서만 로드, 실패 시 solarized-osaka 폴백. iTerm 쪽 경로는 바이트 동일
- 한글 폰트 결함 2단계 수정: 처음엔 JetBrains Mono 주 + D2Coding 폴백으로 잡았으나,
  주 폰트 셀폭(JBM 라틴) 기준 2배 박스에 D2Coding 한글이 얹혀 글자당 약 17% 자간이 떠서
  **D2Coding을 주 폰트로 승격**(JBM은 보조 폴백). 행간은 `adjust-cell-height = 15%`.
  두 폰트 Brewfile 편입, 설치 완료. 교훈: 한글 자간은 폴백으로 못 잡고 주 폰트가 2:1 정합이어야 함
- ssh imac TERM 문제 해결: 원인은 iMac terminfo DB 결손. `~/.terminfo`에
  tmux-256color와 xterm-ghostty를 원격 1회 설치했고 실 ssh로 256색 해석 검증 완료
- Ghostty 테마 심링크(`~/.config/ghostty/themes/reader-dark`)는 이미 생성돼 있음

### 이번 세션에서 한 일원화

축 하나에 정본 하나로 정리했습니다. 정면 충돌이 하나 있었습니다.

- 정본 `좋은 글 작성 기준.md` §4는 설명 문장을 합니다체로 쓰라고 하고, 해라체는 거슬린다는 2026-08-06 피드백을 인용합니다
- `tell-rules.tsv` R03은 `doc` 표면에서 경어체를 금지하고 평서형을 요구했습니다
- 둘 다 같은 날 만들어졌고 정반대였습니다. 정본이 사용자 피드백을 직접 인용하므로 정본을 살렸습니다

조치한 내용입니다.

| 축 | 정본 | 기계 집행 |
|---|---|---|
| 부호(엠대시, 가운뎃점, 슬래시) | `좋은 글 작성 기준.md` §3 대체표 | `ko-style` (`--fix`) |
| 문서 문체와 티의 구조적 원인 | 같은 문서 §1, §2, §4 | 없음(판단 영역) |
| README 특화 | `README 작성 기준.md` | `readme` 스킬 |
| 커밋, PR, 이슈 제목 형태와 계층 | `conventions/commit-message/korean-angularjs.md` | 아직 없음 |
| 파일이 아닌 표면(세션 응답, 커밋)의 티 | `agents/tell-rules.tsv` | `agent-os-tell-lint` |

- `tell-rules.tsv` surfaces 축소: R01, R02는 `chat,commit`으로, R03은 `commit`으로. `.md` 파일의 부호는 `ko-style`이 자동 수정까지 하므로 tell-lint가 중복 검사할 이유가 없습니다
- `korean-angularjs.md` 최상단에 축별 분담표를 넣어 다른 파일 규칙을 옮겨 적지 않도록 했습니다
- `AGENTS.md:10`이 두 정본을 함께 가리킵니다

### 의도적으로 하지 않은 것

- dotfiles 커밋 없음. 네 갈래 변경이 한 워킹트리에 섞여 있어 분리가 필요합니다
- `commit` 표면 훅 미설치. 기준선 측정이 아직 붙이지 말라고 말합니다
- 남의 저장소(nn98) 문서 드리프트 미수정. 발견 목록으로만 전달했습니다
- `release`, `wip` 타입 미추가. 과거 임시 정리 작업의 흔적일 수 있다는 사용자 판단을 따랐습니다

## Decisions (cite, do not restate)

- 확정: `D-008` 공통 지시 50줄 캡. `AGENTS.md`를 교체만 하고 늘리지 않은 이유입니다
- 확정: `D-012` 스크립트 생태 계약. 신규 스크립트는 `scripts.md` 등록 대상입니다
- 확정: `D-015` 핸드오프 문장을 확정 결정으로 인용 금지. 이 노트에도 그대로 적용됩니다
- 확정: `D-026` 워크플로 계층과 superpowers 스코프. 이 세션 초반의 superpowers 조사가 여기로 승격됐습니다
- 확정: `nn98/delivery-discount-api`의 `docs/decisions/ADR-008`. 다만 채택 여부는 동료 판단이며 아직 리뷰 전입니다
- 미결: 말투 규약 개정과 이번 일원화 전체에 D-번호가 없습니다
- 미결: `commit` 표면 훅 도입 여부와 판정 방법
- 미결: R02(가운뎃점) threshold 조정. 문서 기준과 커밋 기준 측정이 모두 조정 여지를 가리킵니다
- 미결: tell-lint의 warn에서 enforce 승격 시점
- 미결: 갈래 4 스킬 동기화의 검수. VENDOR.md 41건이 한꺼번에 바뀌었고 아직 아무도 diff를 읽지 않았습니다
- 미결: Ghostty 대 iTerm2 최종 판정. Brewfile 주석의 A/B는 계속 진행 중이며 이 노트가 판정을 만들지 않습니다
- 미결: nvim reader-dark의 전역 승격 여부(현재는 Ghostty 한정, 사용자 선택), tmux 상태바 리더 테마 전환 여부, 브라우저 리더용 Pretendard 폰트 설치 여부

## Files To Read First

- `~/.obsidian/mimir/20 Knowledge/좋은 글 작성 기준.md`: 한국어 산출물 전체의 정본입니다. 글을 쓰기 전에 먼저 읽습니다
- `agents/conventions/commit-message/korean-angularjs.md`: 축별 분담표와 커밋, PR, 이슈 제목 규칙
- `agents/tell-rules.tsv`: 파일이 아닌 표면의 티 규칙. 새 티는 여기 한 줄 추가가 곧 피드백입니다
- `bin/ko-style`: 부호 검사와 자동 수정. `.md` 저장 시 훅이 자동 실행합니다
- `bin/agent-os-tell-lint`: `chat`과 `commit` 표면 린터
- `~/projects/ww-req/delivery-discount/CLAUDE.md`: 대행 작업 규율
- `~/projects/ww-req/delivery-discount/notes/01_파악과_결정_보고.md`: 동료에게 보낸 파악 결과
- `.config/ghostty/themes/reader-dark`: 터미널 팔레트 정본 이식본. 파생색 근거가 헤더 주석에 있습니다
- `.config/nvim/assets/markdown-reader.css`: 리더 팔레트의 단일 정본. 색을 바꾸려면 여기부터
- `.zshrc` 상단 `_is_ghostty`: 터미널 분기 규약. nvim 쪽 쌍둥이는 `core/term.lua`

## Work In Progress

### Changed files

이번 세션 커밋 완료(`31b8767`):

- `agents/AGENTS.md`(10행 교체, 38행과 44행 엠대시 정리)
- `agents/conventions/commit-message/korean-angularjs.md`, `angular.md`

이번 세션 미커밋:

- `agents/tell-rules.tsv`(surfaces 축소). 파일 자체가 다른 세션 소유의 미추적 파일이라
  제 변경만 떼어 커밋할 수 없습니다. 갈래 3을 커밋할 때 함께 들어가야 합니다
- `docs/conversation/handoff.md`

갈래 5 커밋 완료(`0a2ff9f` 12파일, `0ba7325` 2파일):

- `.config/ghostty/{config,themes/reader-dark}`, `.config/starship.toml`, `.zshrc`,
  `Brewfile`, `install.sh`, `bin/dotfiles-doctor`, `README.md`
- nvim: `colors/reader-dark.lua`, `core/term.lua`, `lazy.lua`, `plugins/ui/{colorscheme,lualine}.lua`
- README은 기능 반영 외에 기존 문장의 엠대시 33건을 `ko-style` 대체표대로 함께 정리했습니다

다른 세션:

- `agent-os/DECISIONS.md`(D-026 신설), `agent-os/scripts.md`, `agent-os/upstreams.md`
- `agents/claude/CLAUDE.md`, `agents/claude/settings-fragment.json`
- `agents/skills/` 41건 수정, 이름 변경 3건(`writing-great-skills`에서 `writing-for-agents`)
- product-loop 관련 4건, `agents/skills/developer-agent-os/SKILL.md`

### Untracked

- `agents/tell-rules.tsv`, `bin/agent-os-tell-lint`, `bin/ko-style`
- `agents/skills/{to-questionnaire,wait-what,wizard}/`, `agents/skills/ask-matt/PHASE-BOUNDARIES.md`, `agents/skills/writing-for-agents/SKILL-MECHANICS.md`
- `bin/notion-job`, `bin/notion-mcp`, `agents/jobs/`, `agents/notion.json`, `agents/skills/meeting-notes/`, launchd plist 2종(이전 세션 잔여)

### 되돌리면 안 되는 상태

- 위 전부입니다. 네 갈래 모두 진행 중이고 커밋 분리만 남았습니다
- `~/projects/ww-req/delivery-discount/*` 세 저장소의 `origin` push URL이 무효값입니다. 의도된 봉쇄입니다

## Verification

- `./gradlew test --rerun-tasks`(delivery-discount-api)
  Result: 75건 전원 통과, 실패 0. `BrandComparisonServiceTest`가 16에서 31로 늘었습니다
- 실데이터 리허설(원장 138건을 실제 코드 경로에 태움)
  Result: 2026-07-30에 브랜드 86개와 오퍼 130건, 2026-08-06에 83개와 125건, 2026-09-01에 68개와 88건. 오늘 기준 만료 5건이 정확히 빠집니다
- `agent-os-tell-lint --surface commit` 소급 측정(저장소 5곳, 커밋 40건씩)
  Result: dotfiles 77% 위반, dref 75%, naon 46%, element-to-markdown 0%(영문), nn98/api 45%. R01과 R02는 기존 커밋 절반 이상을 때립니다. R03은 다섯 곳 모두 0%로 정밀도가 좋습니다
- 일원화 후 회귀 확인
  Result: `ko-style` 기준 `AGENTS.md`와 규약 2종 모두 exit 0. tell-lint `doc` 표면은 exit 0으로 손을 뗐고 `commit` 표면은 R03이 여전히 잡습니다
- dotfiles 테스트 스위트: 실행하지 않았습니다. 이번 변경이 문서와 규칙 파일뿐이고 스크립트 로직을 건드리지 않았기 때문입니다
- 갈래 4 스킬 diff: 읽지 않았습니다. 다른 세션 산출물이고 41개 파일 규모입니다
- 갈래 5 검증(스크립트 확인분):
  `zsh -n`, `ghostty +validate-config`, `starship print-config` 전부 통과.
  nvim 헤드리스 3경로(iTerm은 solarized 유지, Ghostty와 Ghostty+tmux는 reader-dark,
  투명 Normal, NormalFloat `#252b2d`, terminal_color 세팅) 확인.
  zsh 분기 3시나리오에서 BAT_THEME과 fzf 색 정확.
  `TERM=tmux-256color`와 `TERM=xterm-ghostty`로 실 ssh imac 접속, 둘 다 256색 해석.
  Ghostty 폰트 체인이 bold와 italic까지 D2Coding 다음 JetBrains Mono로 해석되고
  adjust-cell-height 15% 반영 확인.
  시각 확인(Ghostty 창에서 실제 렌더링, 한글 폰트 체감)은 사용자 몫으로 남아 있습니다

## Next Steps

1. 남은 갈래를 커밋합니다. 갈래 2는 `31b8767`로 끝났고, 티 배관(갈래 3)과 스킬 동기화(갈래 4)가 남았습니다. 갈래 3을 커밋할 때 `agents/tell-rules.tsv`의 surfaces 축소가 함께 들어갑니다
2. 갈래 4 스킬 동기화를 검수합니다. VENDOR.md 41건 diff와 신규 3종의 내용 확인이 남아 있습니다
3. R02 threshold를 재검토합니다. 사용자 본인 문체이기도 해서 내부 운영 문서 기준으로는 완화 여지가 있습니다
4. 2주 뒤에 신규 커밋만 다시 측정합니다. `git log --since=2026-08-06`에 같은 린트를 돌려 과거 부채와 신규를 분리합니다. 신규 위반율이 0에 수렴하면 `commit` 훅은 불필요합니다
5. 4번 결과에 따라 `agent-os-tell-lint`에 `--hook commit` 추가를 판단합니다. CLI stdin 경로는 ops-event를 남기지 않으므로 관측하려면 약 20줄이 필요합니다
6. 이번 일원화와 말투 규약을 `agent-os/DECISIONS.md`에 D-번호로 승격할지 정합니다
7. nn98 PR 리뷰 대응. 저장소 최초 PR이라 동료가 알림을 못 받았을 수 있습니다
8. `bin/ko-style`이 `scripts.md`에 미등록입니다(D-012 드리프트). `tell-lint`만 등록돼 있습니다
9. 갈래 5 시각 확인: Ghostty에서 cmd+shift+, 리로드 후 프롬프트, fzf(Ctrl+T), `bat`,
   nvim, 한글 렌더링을 눈으로 확인합니다. iTerm은 이전과 동일해야 합니다
10. A/B 판정이 나면 Brewfile의 병행 주석과 CLAUDE.md의 관련 절을 갱신합니다.
   D2Coding 주 폰트(라틴 포함)가 아쉬우면 다음 후보는 Sarasa Term K, Monoplex KR Nerd이며
   행간 15%도 체감에 따라 10~20% 사이에서 조정 여지가 있습니다

## Watch Outs

- 워킹트리에 네 세션 변경이 섞여 있습니다. `git commit -a`를 그냥 부르면 남의 작업이 딸려 들어갑니다
- **index에 다른 세션이 미리 올려둔 변경이 있습니다.** 이번에 실제로 사고가 났습니다. 제 파일 3개만 `git add` 했는데도 커밋에 스킬 이름 변경 3건이 딸려 갔습니다. `git status`에서 첫 열이 `R`이면 이미 스테이징된 상태입니다. 경로를 명시한 `git commit -F <msg> -- <paths>` 형태를 쓰면 index의 나머지를 건드리지 않고 부분 커밋이 됩니다
- 위 사고가 갈래 5에서 한 번 더 재현됐습니다(스킬 리네임 3건이 또 딸려 들어가 `reset --soft` 후 경로 지정 커밋으로 복구). 이 워킹트리에서 커밋할 때는 처음부터 `git commit -- <paths>`를 쓰는 것이 규칙입니다
- Ghostty 분기 감지의 한계: 이미 떠 있는 tmux 서버는 자기를 띄운 터미널 기준으로 판정이 남습니다. A/B 중 터미널을 오가면 `tmux kill-server`로 리셋합니다
- 훅은 이미 활성입니다. 직전 핸드오프에 "다음 세션부터 활성"이라고 적었는데 **틀렸습니다.** 이 세션에서 `AGENTS.md` 편집이 실제로 두 번 막혔고 `ko-style --fix`가 파일을 직접 고쳤습니다
- 훅이 파일을 수정하므로 편집 직후 내용이 달라질 수 있습니다. 오래된 `old_string`으로 다시 편집하려면 먼저 읽어야 합니다
- 규칙 문서가 금지 부호를 그대로 쓰면 훅이 그것까지 고쳐버립니다. 부호를 언급할 때는 인라인 코드로 감쌉니다
- 대행 저장소 금지 사항: `python export_data.py` 실행 절대 금지(원장이 옛 스냅샷으로 덮여 수집분이 소실됩니다). `data/`는 읽기 전용이고 push는 fork 리모트로만 합니다
- 계층을 섞지 않습니다. 남의 저장소 문체를 내 저장소로 들이지 않고, 내 티 규칙을 남의 저장소에 강요하지도 않습니다. nn98 저장소는 줄표를 45% 쓰므로 거기서는 줄표가 집안 문체입니다
- ADR 제목은 서술형 결정문이 정답입니다. 커밋과 통일한다고 명사형으로 바꾸면 의미가 빠집니다
