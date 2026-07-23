# Neovim Configuration Context

이 문서는 `.config/nvim`을 매번 처음부터 분석하지 않기 위한 구조 요약이다.
AI가 이 Neovim 설정을 수정할 때는 먼저 이 문서를 읽고, 실제 Lua 파일을 확인한 뒤 작업한다.

## AI 유지보수 지시

- `.config/nvim`의 구조, 책임 분리, 주요 플러그인, 키맵, LSP/formatter/linter 설치 목록을 바꾸면 이 문서도 함께 갱신한다.
- 새 플러그인을 추가하면 `구조`, `플러그인 구성`, `주요 키맵`, `전문가 평가` 중 영향받는 섹션을 갱신한다.
- 키맵을 바꾸면 충돌 가능성까지 확인하고 `주요 키맵`에 반영한다.
- LSP, Mason, formatter, linter, DAP 관련 변경은 `언어 지원`과 `주의할 점`에 반영한다.
- `lazy-lock.json`은 잠금 파일이므로 플러그인 업데이트 결과 외에는 직접 편집하지 않는다.
- 설정 파일을 수정할 때는 기존 스타일을 우선한다. 현재 Lua 파일은 플러그인별 단일 파일 분리 방식을 사용한다.

## 진입점

```text
.config/nvim/init.lua
  -> require("miniminjae.core")
  -> require("miniminjae.lazy")
```

- `lua/miniminjae/core/init.lua`: 기본 옵션과 전역 키맵을 로드한다.
- `lua/miniminjae/lazy.lua`: `lazy.nvim`을 bootstrap하고 플러그인 디렉터리를 import한다.
- 플러그인 import 경로:
  - `miniminjae.plugins`
  - `miniminjae.plugins.lsp`

## 디렉터리 구조

```text
.config/nvim/
├── assets/
│   └── markdown-reader.css
├── init.lua
├── lazy-lock.json
├── README.md
├── snippets/
│   └── markdown.lua
└── lua/miniminjae/
    ├── lazy.lua
    ├── core/
    │   ├── init.lua
    │   ├── options.lua
    │   └── keymaps.lua
    └── plugins/
        ├── init.lua
        ├── *.lua
        └── lsp/
            ├── mason.lua
            └── lspconfig.lua
```

## Core 설정

`core/options.lua`는 에디터 기본값을 담당한다.

- 줄 번호: `number`, `relativenumber`
- 들여쓰기: 2 spaces, `expandtab`, `autoindent`
- 줄바꿈: `wrap = true`, `linebreak = true`, `showbreak = "↪ "`
- 검색: `ignorecase`, `smartcase`
- UI: `cursorline`, `termguicolors`, `background = "dark"`, `signcolumn = "yes"`
- 클립보드: system clipboard `unnamedplus`
- split 방향: 오른쪽/아래
- swapfile 비활성화
- MDX: `mdx` filetype 등록, Treesitter markdown parser를 mdx에 등록

`core/keymaps.lua`는 전역 키맵과 일부 파일 타입 키맵을 담당한다.

- leader는 `<Space>`
- visual indent 유지: `<`, `>`
- 전체 복사: `<leader>gg`
- 현재 줄 복제: `<S-k>`
- insert 종료: `jk`
- search highlight 제거: `<leader>hh`
- window split: `<leader>sv`, `<leader>sh`, `<leader>se`, `<leader>sx`
- tab: `<leader>to`, `<leader>tx`, `<leader>tn`, `<leader>tp`, `<leader>tf`
- markdown/mdx bold: `<leader>b`
- IntelliJ 스타일 새 줄:
  - `<leader>;`: cosco로 세미콜론/콤마 처리 후 새 줄
  - `<leader>:`: 세미콜론 없이 새 줄

## 플러그인 구성

### 공통 인프라

- `lazy.nvim`: 플러그인 매니저. `lazy.lua`에서 stable branch를 bootstrap한다.
- `plenary.nvim`: 여러 플러그인의 공통 의존성.
- `vim-tmux-navigator`: tmux와 Neovim split 이동 연동.
- `which-key.nvim`: leader 키 힌트. `timeoutlen = 500`.
- `dressing.nvim`: select/input UI 개선.

### UI와 탐색

- `solarized-osaka.nvim`: 기본 colorscheme. dark, transparent 설정.
- `alpha-nvim`: 시작 대시보드. 큰 Unicode 아트와 자주 쓰는 명령 버튼을 제공한다.
- `lualine.nvim`: 상태줄. lazy update count 표시.
- `bufferline.nvim`: buffer 대신 tab 표시 모드.
- `nvim-tree.lua`: 파일 탐색기. `<leader>ee`, `<leader>ef`, `<leader>ec`, `<leader>er`.
- `telescope.nvim`: fuzzy finder. `find_files`, `oldfiles`, `live_grep`, `grep_string`, todo 검색.
- `telescope-fzf-native.nvim`: Telescope fzf native sorter.
- `indent-blankline.nvim`: indent guide.
- `nvim-highlight-colors`: 색상 미리보기. `<leader>tc`로 virtual/background 렌더 전환.

### 편집 UX

- `nvim-autopairs`: 괄호/따옴표 자동 완성, cmp confirm 연동, markdown/mdx fenced code rule 추가.
- `nvim-surround`: surround 조작.
- `substitute.nvim`: `s`, `ss`, `S`를 substitute 동작으로 사용한다.
- `Comment.nvim` + `nvim-ts-context-commentstring`: TSX/JSX/Svelte/HTML 문맥 주석 지원.
- `cosco.vim`: 세미콜론/콤마 자동 삽입. `<leader>;` 키맵에서 직접 호출한다.
- `vim-table-mode`: Markdown table 편집. `<leader>tm`.
- `LuaSnip`: 커스텀 snippets와 friendly snippets 기반.

### Markdown/MDX

- `render-markdown.nvim`: markdown/mdx 렌더링 보조.
- `markdown-preview.nvim`: 브라우저 Markdown preview. Reader UI는 `assets/markdown-reader.css`가 제공하며, `<leader>mp`, `<leader>ms`, `<leader>mt`, `<leader>ml`을 사용한다.
- `img-clip.nvim`: clipboard image paste. `<leader>p`, 이미지 저장 위치는 현재 파일 기준 상대 경로.
- `snippets/markdown.lua`: front matter, 이미지 div, video tag, spacer snippets.

### Git/작업 관리

- `gitsigns.nvim`: hunk 이동/스테이징/reset/blame/diff.
- `lazygit.nvim`: `<leader>lg`.
- `todo-comments.nvim`: TODO/FIXME/NOTE/HACK 탐색. `]t`, `[t`.
- `trouble.nvim`: diagnostics, quickfix, loclist, todo list UI.
- `auto-session`: 수동 session restore/save. `<leader>wr`, `<leader>ws`; 자동 복원은 꺼져 있다.

### HTTP, Debug

- `kulala.nvim`: `.http`, `.rest` 파일용 HTTP client. `<leader>hr`, `<leader>ht`, `[h`, `]h`, `<leader>hs`.
- `nvim-dap`, `nvim-dap-ui`, `nvim-dap-virtual-text`, `telescope-dap.nvim`: DAP UI와 키맵.
  - `<leader>db`, `<leader>dc`, `<leader>di`, `<leader>do`, `<leader>dO`, `<leader>dr`, `<leader>dl`, `<leader>du`, `<leader>dx`
  - IntelliJ 스타일: `<F9>`, `<F8>`, `<F7>`, `<S-F8>`, `<C-F8>`

## 언어 지원

### Mason 설치 목록

`plugins/lsp/mason.lua`가 Mason과 자동 설치 목록을 관리한다.

LSP:

- `html`
- `cssls`
- `tailwindcss`
- `svelte`
- `lua_ls`
- `graphql`
- `emmet_ls`
- `pyright`
- `ts_ls`
- `jdtls`
- `clangd`
- `mdx_analyzer`
- `marksman`

Formatters/linters/debug tools:

- `prettierd`
- `stylua`
- `google-java-format`
- `ruff`
- `eslint_d`
- `java-debug-adapter`
- `java-test`

### LSP 설정

`plugins/lsp/lspconfig.lua`가 공통 LSP keymap과 서버별 설정을 담당한다.

공통 LSP 키맵:

- `gR`: references
- `gD`: declaration
- `gd`: definitions
- `gi`: implementations
- `gt`: type definitions
- `<leader>ca`: code action
- `<leader>rn`: rename
- `<leader>D`: buffer diagnostics
- `<leader>d`: line diagnostic float
- `[d`, `]d`: diagnostic navigation
- `gh`: hover
- `<leader>rs`: LSP restart

서버별 특이점:

- `marksman`: markdown/mdx filetypes.
- `mdx_analyzer`: mdx 전용, TypeScript 검사 활성화.
- `tailwindcss`: markdown/mdx까지 filetypes 확장.
- `clangd`: `--background-index`.
- `svelte`: JS/TS 저장 시 Svelte server에 변경 알림.
- `graphql`: graphql/gql/svelte/react filetypes.
- `emmet_ls`: html, react, css 계열, svelte, mdx.
- `lua_ls`: `vim` global 인식.
- `pyright`: typeCheckingMode `basic`.
- `nvim-jdtls`: Java 전용. Mason의 `jdtls`, `java-test`, `java-debug-adapter`를 사용하고 Lombok javaagent를 포함한다.

### Formatting

`plugins/formatting.lua`는 `conform.nvim`을 사용한다.

- JS/TS/React/Svelte/CSS/HTML/JSON/YAML/Markdown/GraphQL: `prettierd`, fallback `prettier`
- Lua: `stylua`
- Python: `ruff_organize_imports`, `ruff_format`
- Java: `google-java-format`
- format on save 활성화, timeout 1000ms
- 수동 format: `<leader>cf`

### Linting

`plugins/linting.lua`는 `nvim-lint`를 사용한다.

- JS/TS/React/Svelte: `eslint_d`
- Python: `ruff`
- trigger: `BufEnter`, `BufWritePost`, `InsertLeave`
- 수동 lint: `<leader>cl`

### Treesitter

`plugins/treesitter.lua`는 highlight, indent, autotag, incremental selection을 설정한다.

설치 parser:

- json, javascript, typescript, tsx, yaml, html, css, prisma
- markdown, markdown_inline, svelte, graphql, bash
- lua, vim, vimdoc, dockerfile, gitignore, query
- c, cpp, java

## 주요 키맵 충돌과 주의할 점

- `<leader>hr`, `<leader>hs`, `[h`, `]h`는 `gitsigns.nvim`과 `kulala.nvim` 양쪽에서 사용한다. `kulala.nvim`은 `ft = { "http", "rest" }`라 HTTP 파일에서만 로드되지만, HTTP 파일에서 Git hunk 키맵과 의미가 겹칠 수 있다.
- `substitute.nvim`이 normal/visual `s`를 대체한다. 기본 `s` 동작을 기대하는 사용자는 혼동할 수 있다.
- `core/options.lua`의 `opt.wrap = true` 주석은 "disable line wrapping"이라고 되어 있지만 실제 동작은 wrap 활성화다. 주석만 부정확하다.
- `nvim-tree.lua`에서 netrw를 끄지만 `options.lua`에는 `g:netrw_liststyle = 3`가 남아 있다. 기능상 큰 문제는 아니지만 의미가 중복된다.
- `lualine.lua`의 inactive 색상은 `colors.semilightgray`를 참조하지만 `colors` 테이블에 정의되어 있지 않다. lualine이 nil을 허용하면 눈에 띄지 않을 수 있으나 정리 후보이다.
- `nvim-jdtls` 설정은 macOS의 `config_mac`을 전제로 한다. Linux 환경으로 옮기면 configuration 경로 분기가 필요하다.
- `mason_registry.refresh` callback 안에서 jdtls를 시작하므로 Java 파일 첫 진입 시 비동기 타이밍을 고려해야 한다.
- `dap.lua`는 UI와 키맵만 정의하고 언어별 adapter 설정은 Java 외에는 없다. 다른 언어 디버깅을 기대하면 adapter 구성이 추가로 필요하다.
- `markdown-preview.nvim`의 build가 `cd app && yarn install`이라 Node/Yarn이 필요하다.
- `markdown-preview.nvim`의 custom Markdown CSS는 기본 `markdown.css`에 덧붙지 않고 교체된다. Reader CSS를 수정할 때는 이 파일이 독립적으로 필요한 기본 스타일을 모두 제공해야 한다.
- `telescope-fzf-native.nvim`와 `LuaSnip` jsregexp build는 `make`가 필요하다.

## 전문가 평가

전체적으로 개인용 dotfiles Neovim 설정으로는 좋은 편이다. 진입점이 얇고, `core`, `plugins`, `plugins/lsp`로 책임이 분리되어 있으며, 플러그인별 파일 분리 덕분에 다른 AI나 사람이 수정 범위를 좁히기 쉽다. Markdown/MDX 작성, FE 개발, Python, Java, C/C++까지 다루는 실사용 중심 구성이며 Mason, conform, nvim-lint, nvim-cmp, Treesitter 조합도 현대적인 편이다.

강점:

- `lazy.nvim` import 구조가 명확해서 플러그인 추가/삭제가 쉽다.
- LSP attach keymap을 autocmd로 묶어 buffer-local하게 적용한다.
- Mason 설치 목록이 LSP와 외부 도구를 한 곳에서 관리한다.
- Markdown/MDX 생산성 설정이 풍부하다. render, preview, image paste, snippet, table mode가 함께 구성되어 있다.
- Java는 `nvim-jdtls`, DAP, test bundle까지 고려되어 있어 단순 lspconfig보다 실전성이 높다.

개선 우선순위:

1. `lspconfig.lua`가 너무 길다. Java `nvim-jdtls` 설정을 `plugins/lsp/java.lua`로 분리하면 유지보수성이 크게 좋아진다.
2. 키맵 네임스페이스를 정리할 가치가 있다. 특히 `<leader>h`가 Git hunk와 HTTP request에 동시에 쓰이고, `<leader>t`가 tab/test/table/color 등으로 퍼져 있다.
3. `which-key.nvim` group label을 명시하면 현재 많은 leader 키맵을 더 발견하기 쉬워진다.
4. `format_on_save` timeout 1000ms는 큰 Java/Markdown/Prettier 프로젝트에서 실패할 수 있다. 실제 사용 중 timeout이 보이면 2000ms 전후로 조정할 만하다.
5. 주석과 실제 옵션이 다른 부분, 정의되지 않은 color key 등 작은 불일치를 정리하면 AI가 오해할 가능성이 줄어든다.
6. `neodev.nvim`는 Neovim Lua 개발용으로 오래 쓰였지만 최신 생태계에서는 `lazydev.nvim` 전환을 검토할 수 있다. 단, 작동 중인 설정이면 즉시 바꿀 필요는 없다.

권장 변경 방식:

- 작은 플러그인 추가는 `lua/miniminjae/plugins/<name>.lua`에 새 파일로 추가한다.
- LSP 서버 추가는 `mason.lua`의 `ensure_installed`와 `lspconfig.lua`의 handler를 함께 확인한다.
- formatter/linter 추가는 Mason tool 설치 목록과 `formatting.lua`/`linting.lua`를 함께 수정한다.
- Java 관련 변경은 `nvim-jdtls`의 Mason package 경로, workspace 경로, bundle glob, root detection을 같이 검토한다.
- Markdown/MDX 관련 변경은 `options.lua`, `render-markdown.lua`, `markdown-preview.lua`, `img-clip.lua`, `luasnip.lua`, `snippets/markdown.lua`의 상호작용을 함께 확인한다.

## 빠른 작업 가이드

- 플러그인 상태 확인: `:Lazy`
- Mason 설치 확인: `:Mason`
- Mason 목록 설치: `:MasonInstallAll`
- LSP 상태 확인: `:LspInfo`
- Treesitter 설치 확인: `:TSInstallInfo`
- format 수동 실행: `<leader>cf`
- lint 수동 실행: `<leader>cl`
- diagnostics UI: `<leader>xw`, `<leader>xd`
- 파일 탐색: `<leader>ee`
- fuzzy find: `<leader>ff`, `<leader>fs`
- Markdown preview: `<leader>mp` 열기, `<leader>ms` 중지, `<leader>mt` 토글, `<leader>ml` 라이트/다크 전환
