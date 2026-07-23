# Agent Handoff — Neovim Markdown Reader

## Context

- Date: 2026-07-23
- Repository: `/Users/miniminjae/.dotfiles`
- Branch: `main`
- User goal: 기존 `iamcco/markdown-preview.nvim`을 유지하면서, 자주 읽어도 피로하지 않은 고가독성 Reader UI와 라이트/다크 전환을 만든다.

## Execution Profile

- 작업 등급: `worker`
- 권장 실행자: `gpt-5.6-terra` low/medium
- `gpt-5.6-luna` 실행 범위:
  - 아래 명세대로 CSS·Lua·README를 구현하고 기계 검증하는 데는 충분하다.
  - 디자인을 임의로 재해석하거나 새 플러그인을 비교·도입하지 않는다.
  - 실제 브라우저 결과를 한 번 렌더링한 뒤 사용자 시각 확인 지점에서 멈춘다.
- 독립적인 위임 단위가 아니므로 하위 에이전트를 추가하지 않는다.
- 가장 빠른 경로는 이 인계 없이 현재 세션에서 구현하는 것이지만, 이 문서는 저비용 새 세션 실행을 위해 요구사항을 닫아 둔 것이다.

## Launch Recommendation

### 권장: 컨텍스트를 유지하면서 실행 모델만 낮추기

1. 현재 Codex CLI에서 `/fork`
2. 분기된 대화에서 `/model`
3. `gpt-5.6-terra`, reasoning `medium` 선택
4. 다음 프롬프트 실행:

```text
docs/conversation/2026-07-23-neovim-markdown-reader-handoff.md를 읽고
Implementation Contract 전체를 구현하고 Verification 순서대로 검증해.
기존 dirty state는 건드리지 마.
```

- `/fork`가 현재 대화 기록을 보존하므로 `/new`보다 재설명 위험이 작다.
- 이 작업은 단일 구현과 시각 검증이 강하게 연결돼 있어 한 주 에이전트가 끝까지 맡는 편이 낫다.

### 최저 비용: 완전히 새 Luna 세션

1. `/new`
2. `/model`에서 Luna와 지원되는 낮은 reasoning 선택
3. 위 프롬프트를 그대로 실행

- 현재 `agents/routing.json`과 `.codex/agents/worker.toml`에는 Luna가 일반 worker로 등록돼 있지 않다.
- `/model` 메뉴에 Luna가 노출되는 환경에서만 이 경로를 사용한다.
- Luna는 명세 구현과 기계 검증까지만 맡고, 최종 타이포그래피는 사용자 시각 확인을 거친다.

### 현재 Sol 세션에서 서브에이전트로 실행

- 가능한 프롬프트:

```text
worker 서브에이전트 하나에게
docs/conversation/2026-07-23-neovim-markdown-reader-handoff.md의 구현과 검증을 맡겨.
완료되면 네가 변경 범위와 검증 결과만 최종 확인해.
```

- 현재 로컬 worker 설정은 `gpt-5.6-terra`, reasoning `low`다.
- 부모 Sol과 worker가 모두 토큰을 사용하므로 `/fork` 후 Terra 단독 실행보다 비용 효율은 낮다.
- 병렬화할 독립 작업이 없으므로 이번 작업의 기본 경로로는 권장하지 않는다.

## Current State

- 이미 설치된 브라우저 프리뷰: `iamcco/markdown-preview.nvim`
- 이미 설치된 인버퍼 렌더러: `MeanderingProgrammer/render-markdown.nvim`
- Markdown 프리뷰 설정은 키맵 외에는 거의 기본값이다.
- 플러그인은 다음 기능을 이미 제공한다.
  - 브라우저 라이브 갱신과 동기 스크롤
  - 라이트/다크 테마
  - `mkdp_markdown_css`를 통한 전체 Markdown CSS 교체
  - `mkdp_highlight_css`를 통한 코드 하이라이트 CSS 교체
- 브라우저 테마 스위치는 파일명 헤더에 마우스를 올릴 때만 React DOM에 생성된다.
- 이번 조사에서는 `.config/nvim` 파일을 수정하지 않았고 테스트도 실행하지 않았다.

## Key Decisions

- Decision: 현재 `markdown-preview.nvim`을 유지한다.
  Reason: 새 의존성과 기능 회귀 없이 타이포그래피를 CSS로 완전히 제어할 수 있다.
- Decision: 별도 플러그인(`github-preview.nvim`, `peek.nvim`, `markview.nvim`)을 추가하지 않는다.
  Reason: 이번 목표는 플러그인 비교가 아니라 현재 프리뷰의 독서 품질 향상이다.
- Decision: Reader CSS는 저장소 안에 독립 파일로 둔다.
  Reason: dotfiles와 함께 이식되고 `stdpath("config")`로 안정적인 절대 경로를 만들 수 있다.
- Decision: 플러그인 설치 캐시와 빌드 산출물은 수정하지 않는다.
  Reason: 업데이트 때 사라지는 생성 상태이며 사용자 안전 규칙에도 맞지 않는다.
- Decision: 브라우저 스위치를 CSS만으로 항상 표시하려 하지 않는다.
  Reason: hover 밖에서는 해당 DOM 자체가 존재하지 않는다. 대신 hover 컨트롤을 명확하게 스타일링하고 Neovim 테마 토글 키맵을 제공한다.

## Files To Read First

- `.config/nvim/README.md`: Neovim 구조, Markdown 관련 변경 규칙, 문서 갱신 의무
- `.config/nvim/lua/miniminjae/plugins/markdown-preview.lua`: 현재 플러그인 설정과 `<leader>mp/ms/mt` 키맵
- `.config/nvim/lua/miniminjae/plugins/render-markdown.lua`: 기존 인버퍼 렌더러와 역할 중복 방지
- `install.sh`: `.config/nvim` 전체 디렉터리를 `~/.config/nvim`으로 연결하는 방식
- `agents/AGENTS.md`: 사용자 변경 보호와 dotfiles 작업 규칙

## Implementation Contract

### 1. Reader CSS 추가

- 새 파일: `.config/nvim/assets/markdown-reader.css`
- 외부 CDN, 원격 폰트, JavaScript를 사용하지 않는다.
- `mkdp_markdown_css`는 기본 `markdown.css`에 덧붙이는 것이 아니라 교체한다. 따라서 새 CSS는 독립적으로 완결돼야 한다.
- 기존 `highlight.css`는 유지한다. `mkdp_highlight_css`는 설정하지 않는다.
- DOM 기준:
  - 전체 테마: `[data-theme="dark"]`
  - 본문: `.markdown-body`
  - 컨테이너: `#page-ctn`
  - 헤더: `#page-header`
  - hover 시 테마 컨트롤: `#toggle-theme`

### 2. 시각 명세

- 본문 최대 폭: `760px` 전후
- 본문 글자: `18px`
- 줄높이: `1.8`
- 본문 폰트 순서:
  - `"Pretendard Variable"`
  - `Pretendard`
  - `-apple-system`
  - `BlinkMacSystemFont`
  - `"Apple SD Gothic Neo"`
  - `"Noto Sans KR"`
  - sans-serif
- 코드 폰트 순서:
  - `"JetBrains Mono"`
  - `"SFMono-Regular"`
  - `Consolas`
  - monospace
- 코드 글자: `14.5px`에서 `15px`
- 문단 간격: 최소 `1.15em`
- 제목:
  - 본문과 확실한 크기·굵기·상하 간격 차이를 둔다.
  - `h1`, `h2`만 얇은 하단 경계를 사용한다.
  - 지나치게 화려한 아이콘이나 그라디언트는 쓰지 않는다.
- 표:
  - 가로 스크롤 가능
  - 헤더 배경과 셀 경계가 두 테마 모두에서 분명해야 한다.
- 인용문:
  - 왼쪽 accent border
  - 본문보다 약간 흐린 색
  - 배경 대비는 낮게 유지한다.
- 인라인 코드와 코드 블록을 구분한다.
- 이미지:
  - `max-width: 100%`
  - 적당한 radius
- 좁은 화면에서는 본문 좌우 padding을 줄이는 media query를 둔다.
- 모션은 필수가 아니며, 넣더라도 `prefers-reduced-motion`을 존중한다.

### 3. 색상 명세

- CSS custom properties로 라이트/다크 팔레트를 한곳에서 관리한다.
- 라이트:
  - 완전 흰 캔버스 대신 따뜻한 오프화이트 계열
  - 본문은 진한 회갈색 계열
  - WCAG AA 수준의 본문 대비를 유지한다.
- 다크:
  - 완전 검정 대신 짙은 먹색/차콜 계열
  - 본문은 순백색보다 부드러운 아이보리 계열
  - 링크, 인라인 코드, 표 경계가 배경에 묻히지 않아야 한다.
- Solarized 색을 그대로 복제할 필요는 없지만 현재 Neovim의 `solarized-osaka`와 함께 두었을 때 이질적이지 않아야 한다.

### 4. Lua 설정

`.config/nvim/lua/miniminjae/plugins/markdown-preview.lua`의 기존 구조와 tab 스타일을 유지한다.

- `init`에서 다음 경로를 설정한다.
  - `vim.g.mkdp_markdown_css = vim.fn.stdpath("config") .. "/assets/markdown-reader.css"`
- 초기 테마:
  - `vim.o.background == "light"`이면 `light`
  - 그 외에는 `dark`
- 기존 `<leader>mp`, `<leader>ms`, `<leader>mt`는 유지한다.
- 새 키맵: `<leader>ml`
  - 설명: `Toggle Markdown Preview Light/Dark`
  - 현재 `vim.g.mkdp_theme`을 `light`와 `dark` 사이에서 전환한다.
  - 실행 중인 프리뷰가 새 테마를 확실히 읽도록 `MarkdownPreviewStop` 후 짧은 `vim.defer_fn`으로 `MarkdownPreview`를 다시 연다.
  - 전환된 테마를 `vim.notify`로 알려준다.
- 지속 설정 파일이나 새 상태 파일은 만들지 않는다.
- MDX 지원 확대 등 범위 밖 설정은 건드리지 않는다.

### 5. 문서 갱신

`.config/nvim/README.md`의 다음 내용만 갱신한다.

- Markdown/MDX 플러그인 설명에 Reader CSS 경로와 역할 추가
- 주요 키맵에 `<leader>ml` 추가
- 주의할 점에 custom Markdown CSS가 기본 CSS를 교체한다는 사실 추가
- 디렉터리 트리에 `assets/markdown-reader.css` 추가

루트 `README.md`는 현재 사용자 변경이 있으므로 이번 작업에서 수정하지 않는다.

## Work In Progress

- 이 인계 파일만 새로 추가됐다.
- 기존 dirty state는 사용자 또는 다른 세션 작업이다. 되돌리거나 정리하지 않는다.
  - `README.md`
  - `agent-os/paths.env`
  - `agents/AGENTS.md`
  - `bin/agent-notify`
  - `bin/agent-os-usage`
  - `bin/asx`
  - `tests/test_agent_notify.py`
  - `agents/skills/lms-harvest/`
  - `agents/skills/teach/`
  - `agents/skills/term/`
  - `nvim.log`
  - `tests/test_agent_os_usage.py`
  - `tests/test_asx.py`
- 기존 `docs/conversation/handoff.md`는 다른 활성 작업을 담고 있다. 덮어쓰지 않는다.

## Verification

구현 후 아래 순서로 검증한다.

1. 변경 범위:
   - `git status --short -- .config/nvim docs/conversation/2026-07-23-neovim-markdown-reader-handoff.md`
   - `.config/nvim`과 이 인계 파일 외 변경이 없어야 한다.
2. CSS 경로:
   - Neovim headless에서 `vim.g.mkdp_markdown_css`가 존재하고 `vim.fn.filereadable(...) == 1`인지 확인한다.
3. 키맵:
   - Markdown filetype을 연 상태에서 `<leader>mp/ms/mt/ml` 매핑이 모두 존재하는지 확인한다.
4. 렌더링 fixture:
   - `/tmp` 아래 임시 Markdown 파일에 한글 장문, h1-h4, 중첩 목록, 체크박스, 인용문, 링크, 인라인 코드, 코드 블록, 표, 이미지, Mermaid를 넣는다.
   - fixture는 저장소에 남기지 않는다.
5. 실제 브라우저:
   - `<leader>mp`로 열고 1440px와 약 900px 폭에서 본문을 확인한다.
   - `<leader>ml`로 라이트/다크를 각각 열어 색상 대비, 표, 코드, 링크를 확인한다.
   - 동기 스크롤과 라이브 갱신이 기존처럼 작동하는지 확인한다.
6. 사용자 시각 확인:
   - 구현자가 Luna라면 두 테마의 렌더링 성공까지 보고하고, 미세 색상·글자 크기는 사용자 확인 전 임의로 반복 조정하지 않는다.

## Acceptance Criteria

- 새 플러그인이나 시스템 의존성이 추가되지 않는다.
- 한글 장문을 10분 이상 읽기 좋은 폭·글자 크기·줄높이를 갖는다.
- 라이트와 다크 모두 본문, 링크, 코드, 인용문, 표가 명확히 구분된다.
- `<leader>ml` 한 번으로 테마가 바뀐 프리뷰를 다시 열 수 있다.
- 기존 `<leader>mp/ms/mt`, 라이브 갱신, 동기 스크롤이 유지된다.
- 플러그인 설치 캐시, `lazy-lock.json`, unrelated dirty files를 수정하지 않는다.
- `.config/nvim/README.md`가 실제 설정과 일치한다.

## Watch Outs

- `mkdp_markdown_css`는 additive override가 아니라 기본 Markdown CSS 전체 교체다.
- `#toggle-theme`는 hover할 때만 생성되므로 CSS로 항상 보이게 만들 수 없다.
- 플러그인 캐시 아래 `app/_static/*.css`, React source, 빌드 산출물을 수정하지 않는다.
- 브라우저의 로컬 폰트 유무에 따라 Pretendard 또는 JetBrains Mono가 fallback될 수 있다. 폰트 설치는 이번 범위가 아니다.
- 미관 개선을 이유로 `render-markdown.nvim`, colorscheme, 전역 Neovim 배경 설정을 바꾸지 않는다.
