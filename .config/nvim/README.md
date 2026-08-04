# Neovim 설정

IntelliJ급 자바 개발을 터미널에서 하되, **모든 조각이 왜 있는지 설명할 수 있는 상태**로 유지하는 것이 이 설정의 목표다.
파일마다 머리에 한 줄짜리 "왜" 주석이 붙어 있다. 그 주석과 이 문서가 어긋나면 둘 중 하나가 낡은 것이다.

- Neovim 0.11+ 네이티브 기능을 우선한다. 플러그인은 내장이 못 하는 일만 맡는다.
- 한 가지 일은 한 곳에서만 한다. 예: 포맷은 conform만, 검색은 fzf-lua만.
- 새 언어를 붙이는 비용이 파일 한두 개를 넘지 않아야 한다.

## 구조

```
.config/nvim/
├── init.lua                  진입점. core → lazy 순서만 정한다
├── lua/miniminjae/
│   ├── core/                 플러그인 없이도 성립하는 층
│   │   ├── options.lua       내장 옵션
│   │   ├── keymaps.lua       전역 키맵 (leader 정의 포함)
│   │   ├── autocmds.lua      파일종류별 규칙
│   │   └── lsp.lua           진단 표시 · lsp/ 등록 · vim.lsp.enable · LspAttach 키맵
│   ├── lazy.lua              lazy.nvim 부트스트랩과 스펙 수집
│   └── plugins/
│       ├── ui/               보이는 것 — colorscheme, lualine, bufferline, snacks, colorizer
│       ├── editor/           움직이는 것 — fzf-lua, oil, gitsigns, trouble, persistence,
│       │                     which-key, todo-comments, 마크다운 4종, kulala, diffview,
│       │                     grug-far, obsidian, dadbod, maximizer
│       ├── coding/           쓰는 것 — blink.cmp, conform, nvim-lint, surround, mini.pairs,
│       │                     ts-comments, substitute, cosco, ts-autotag
│       ├── lang/             언어별 — java.lua
│       ├── lsp.lua           mason(도구 공급) + nvim-lspconfig(데이터원) + lazydev
│       ├── treesitter.lua    파서 설치와 하이라이팅 켜기
│       ├── dap.lua           디버깅 공통층 (어댑터 없음)
│       └── test.lua          neotest 공통층 (어댑터 없음)
├── lsp/                      서버별 오버라이드 (한 서버 = 한 파일)
├── ftplugin/java.lua         jdtls 기동 — 이 설정에서 가장 조심스러운 파일
├── snippets/                 직접 만든 스니펫 (VSCode JSON 형식)
└── assets/                   markdown-preview용 CSS
```

### 층위를 나눈 이유

`dap.lua`와 `test.lua`는 **어댑터가 없다**. 그래서 그 파일만으로는 아무것도 디버깅·실행하지 못한다.
어댑터는 `lang/<언어>.lua`가 꽂는다. 언어를 지우면 그 언어의 디버깅·테스트도 같이 사라지고, 공통층은 손댈 필요가 없다.

## 부팅 순서

1. `init.lua` → `core/`(옵션·키맵·자동명령) — 여기까지는 플러그인이 하나도 없어도 동작한다.
2. `lazy.lua` → 플러그인 스펙 수집. `snacks`·`oil`·`treesitter`·`mason`·colorscheme은 시작할 때 올라오고 나머지는 필요할 때 붙는다.
3. 파일을 열면 `nvim-lspconfig`가 로드되며 `core/lsp.lua`를 실행한다 → 진단 설정, `lsp/*.lua` 등록, `vim.lsp.enable`.
4. 자바 파일이면 추가로 `ftplugin/java.lua`가 그 버퍼의 프로젝트 루트를 계산해 jdtls를 붙인다.

## LSP를 다루는 방식

mason-lspconfig를 **쓰지 않는다**. 이전 설정에서 그것이 설치된 서버를 전부 자동으로 켜면서
jdtls가 두 번 기동됐고(`vim.lsp` 경로 + `nvim-jdtls` 경로), 워크스페이스가 프로젝트마다 어긋났다.

지금은 이렇게 나뉜다.

| 역할 | 담당 |
| --- | --- |
| 서버 바이너리 설치 | `mason.nvim` + `mason-tool-installer` |
| 서버 기본값(cmd·root_markers·filetypes) | `nvim-lspconfig` — 데이터로만 읽는다. `setup()`은 호출하지 않는다 |
| 내 오버라이드 | `lsp/<서버>.lua` |
| 켜기 | `core/lsp.lua`의 `vim.lsp.enable({...})` |
| 자바 | 목록에 없다. `ftplugin/java.lua`가 전담한다 |

`core/lsp.lua`는 `lsp/*.lua`를 읽어 `vim.lsp.config()`로 **다시 등록한다**. 파일만 두면 안 되기 때문이다 —
같은 이름의 `lsp/` 파일은 runtimepath 뒤쪽이 이기는데 nvim-lspconfig가 우리 뒤에 있어서, 그냥 두면 기본값이 내 설정을 덮는다.

### 새 언어 추가 절차

1. `plugins/lsp.lua`의 `ensure_installed`에 mason 패키지 이름을 넣는다.
2. 기본값을 바꿔야 하면 `lsp/<서버>.lua`를 만든다. (안 바꿔도 되면 건너뛴다.)
3. `core/lsp.lua`의 `vim.lsp.enable` 목록에 서버 이름 한 줄.
4. `plugins/treesitter.lua`의 파서 목록에 언어 한 줄.
5. 디버깅·테스트가 필요하면 `plugins/lang/<언어>.lua`를 만들어 어댑터를 꽂는다.

자바처럼 프로젝트 루트를 버퍼마다 다시 계산해야 하는 언어만 `ftplugin/`으로 간다. 나머지는 3번에서 끝난다.

## 키맵

`<leader>` = `Space`. `which-key`가 그룹 이름을 띄우므로 외우지 못해도 leader를 누르고 기다리면 된다.
`<leader>?`는 지금 버퍼에서 쓸 수 있는 키만 보여준다.

> **주의:** `<leader>tt`(터미널)과 `<leader>Tt`(테스트)는 대소문자만 다르다. 대문자 `T`는 전부 테스트다.

### 이동·편집 (leader 없음)

| 키 | 하는 일 |
| --- | --- |
| `jk` | 삽입 모드 나가기 |
| `-` | 상위 폴더를 oil로 열기 (파일 이름 바꾸기·옮기기를 버퍼 편집으로) |
| `s` / `ss` / `S` | 모션 범위 / 한 줄 / 줄 끝까지를 레지스터 내용으로 치환 |
| `ys` `cs` `ds` | 감싸기 / 감싼 것 바꾸기 / 감싼 것 지우기 |
| `gc` | 주석 토글 (내장 + ts-comments가 문법 섞인 파일 처리) |
| `<S-k>` | 현재 줄 아래로 복제 |
| `gl` | 줄 진단 띄우기 |
| `[d` / `]d` | 이전 / 다음 진단 |
| `[h` / `]h` | 이전 / 다음 git 헝크 |
| `[t` / `]t` | 이전 / 다음 TODO |
| `<C-hjkl>` | 분할·tmux 페인 이동 |

### LSP (파일에 서버가 붙었을 때만)

| 키 | 하는 일 |
| --- | --- |
| `gd` | 정의로 (여러 개면 fzf-lua 목록) |
| `gD` | 선언으로 |
| `gR` | 참조 목록 |
| `gi` | 구현 목록 |
| `gt` | 타입 정의 |
| `gh` | 문서 보기 |
| `<leader>ca` | 코드 액션 |
| `<leader>rn` | 이름 바꾸기 |
| `<leader>rs` | LSP 재시작 |
| `<leader>ch` | 인레이 힌트 토글 |

### 완성 (삽입 모드, blink.cmp)

| 키 | 하는 일 |
| --- | --- |
| `<C-j>` / `<C-k>` | 다음 / 이전 후보 |
| `<CR>` | 고른 후보 확정 |
| `<C-Space>` | 완성 띄우기 / 문서 토글 |
| `<C-e>` | 닫기 |
| `<C-u>` / `<C-d>` | 문서 스크롤 |
| `<C-l>` / `<C-h>` | 스니펫 다음 / 이전 자리 |

아무것도 미리 선택돼 있지 않다. 엔터를 잘못 눌러 엉뚱한 후보가 박히는 일을 막기 위해서다.

### leader 그룹

| 그룹 | 키 | 하는 일 |
| --- | --- | --- |
| **찾기 f** | `ff` `fr` `fs` `fc` | 파일 / 최근 파일 / 문자열 / 커서 단어 |
| | `fb` `fk` `fh` `fg` `ft` | 버퍼 / 키맵 / 도움말 / 변경된 파일 / TODO |
| **탐색기 e** | `ee` `ef` | 트리 토글 / 현재 파일 위치 열기 |
| **코드 c** | `cf` `cl` `ca` `ch` `co` | 포맷 / 린트 / 코드 액션 / 인레이 힌트 / import 정리(자바) |
| **git 헝크 h** | `hs` `hr` `hS` `hR` `hu` | 스테이징 / 되돌리기 / 파일 전체 / 스테이징 취소 |
| | `hp` `hb` `hB` `hd` `hD` | 미리보기 / blame / blame 상시 / diff / 직전 커밋과 diff |
| | `hh` | 검색 하이라이트 지우기 |
| **git 리뷰 g** | `gd` `gf` `gq` | 변경분 리뷰 / 이 파일 히스토리 / 닫기 |
| | `gg` `aa` | 파일 전체 복사 / 전체 선택 |
| **디버그 d** | `db` `dc` `di` `do` `dO` | 중단점 / 계속 / 안으로 / 다음 줄 / 밖으로 |
| | `dr` `dl` `du` `dx` `de` | REPL / 다시 실행 / UI / 종료 / 값 평가 |
| **테스트 T** | `Tt` `Tf` `Ta` `Td` `Ts` `To` | 근처 / 파일 / 전체 / 디버그 / 요약 / 출력 |
| | `TN` `TC` | jdtls 자체 실행기 (neotest가 못 잡을 때) |
| **자바 j** | `jr` `jb` | 이 파일만 실행(JEP 330) / `gradlew build` |
| **진단 x** | `xw` `xd` `xq` `xl` `xt` | 프로젝트 / 이 파일 / quickfix / loclist / TODO |
| **창 s** | `sv` `sh` `se` `sx` `sm` | 세로 / 가로 / 균등 / 닫기 / 최대화 |
| | `sr` `sw` | 전역 찾아 바꾸기 / 커서 단어 전역 바꾸기 |
| **탭·토글 t** | `to` `tx` `tn` `tp` `tf` | 새 탭 / 닫기 / 다음 / 이전 / 현재 버퍼를 새 탭으로 |
| | `tt` `tm` `tc` | 터미널 / 표 모드 / 색 표시 방식 |
| **세션 w** | `wr` `wl` `ws` `wd` | 이 디렉터리 복원 / 마지막 복원 / 저장 / 저장 안 함 |
| **마크다운 m** | `mp` `ms` `mt` `ml` | 미리보기 시작 / 중지 / 토글 / 밝기 |
| **옵시디언 o** | `on` `oo` `os` `od` | 새 노트 / 바로 열기 / 검색 / 오늘 일간 노트 |
| | `ot` `ob` `ol` `ow` | 템플릿 / 백링크 / 나가는 링크 / 볼트 전환 |
| **HTTP k** | `kr` `kt` `ks` | 요청 실행 / 헤더·본문 전환 / 스크래치패드 (`.http` 버퍼에서만) |
| **기타** | `lg` `p` `;` `:` `b` | lazygit / 이미지 붙여넣기 / 문장 완성 / 새 줄 / 볼드(마크다운) |

### 탐색기 안에서 (`<leader>ee`)

`snacks.explorer`는 파일 트리처럼 보이지만 **picker 위에서 도는 목록**이다. 그래서 nvim-tree나
NERDTree와 손버릇이 다르다. 열면 목록에 바로 포커스가 가고, 글자를 치면 명령이 아니라
**파일명 필터**가 걸린다. 필터를 지우려면 지운 만큼 지워야 한다.

아래 키는 **which-key에 뜨지 않는다.** picker가 자기 창에만 거는 키맵이라 전역 키맵 목록에
없기 때문이다. 이 표가 그 자리를 대신한다.

| 키 | 하는 일 |
| --- | --- |
| `l` / `h` | 열기(파일이면 편집, 폴더면 펼치기) / 폴더 접기 |
| `<BS>` | 트리 루트를 상위 디렉터리로 |
| `.` | 커서 위치의 디렉터리를 트리 루트로 |
| `Z` | 펼친 폴더 전부 접기 |
| `a` `d` `r` | 새로 만들기(끝에 `/`를 붙이면 폴더) / 지우기 / 이름 바꾸기 |
| `c` `m` | 고른 파일을 지금 디렉터리로 복사 / 옮기기 (고른 게 없으면 `m`은 이름 바꾸기) |
| `y` `p` | 경로를 레지스터로 / 레지스터에 담긴 파일을 여기로 복사 |
| `o` | 시스템 기본 앱으로 열기 |
| `u` | 트리 새로고침 |
| `H` / `I` | 숨김 파일 / gitignore 대상 표시 토글 |
| `P` | 미리보기 창 토글 |
| `<leader>/` | 이 디렉터리 안에서 grep |
| `<C-c>` | 이 디렉터리로 `:tcd` (작업 디렉터리 옮기기) |
| `]g` `[g` | 다음 / 이전 git 변경 |
| `]d` `[d` | 다음 / 이전 진단 |
| `q` | 닫기 (`<Esc>`는 닫지 않는다) |

`c`·`m`·`y`는 여러 개를 골라둔 상태를 전제로 한다. 고르기는 picker 공통 키인 `<Tab>`이다.

**파일을 여러 개 손볼 거면 `-`(oil)이 낫다.** oil은 디렉터리를 그냥 버퍼로 열어서 이름 바꾸기·
옮기기·지우기를 텍스트 편집으로 하고 `:w` 한 번에 적용한다. explorer는 훑어보다 한두 개
건드리는 쪽이고, 대량 정리는 oil 쪽이 손이 덜 간다.

### IntelliJ 손버릇

| 키 | 하는 일 |
| --- | --- |
| `<CR>` / `<BS>` | 선택을 문법 단위로 넓히기 / 좁히기 (Ctrl+W, Ctrl+Shift+W 자리) |
| `F9` / `F8` / `F7` / `Shift-F8` | 계속 / 다음 줄 / 안으로 / 밖으로 |
| `Ctrl-F8` | 중단점 토글 |
| `crV` `crC` `crM` | 변수 / 상수 / 메서드로 추출 (자바) |
| `<leader>;` | 문장 끝에 `;` 붙이고 다음 줄 (Ctrl+Shift+Enter 자리) |
| `<leader>:` | 커서 위치와 무관하게 아래에 새 줄 (Shift+Enter 자리) |

`<CR>`은 노멀 모드에서 커서 아래 낱말부터 잡고, 누를수록 문법 트리를 타고 넓어진다.
`compute` → `compute(1, 2)` → `x = compute(1, 2)` → `int x = compute(1, 2);` 순이다.
`<BS>`는 넓혀온 이력을 그대로 되감아 좁힌다. 트리를 다시 내려가는 게 아니라 스택을 되감는
방식이라 확장의 정확한 역순이 보장된다.

파서가 붙은 일반 파일 버퍼에서만 걸린다. 도움말의 `<CR>`(태그 점프)이나 quickfix의
`<CR>`(항목 열기)은 그대로 살아 있다.

## Java

`ftplugin/java.lua`가 자바 버퍼마다 실행된다. 핵심은 **루트를 그때그때 다시 계산하는 것**이다.

루트는 단계적으로 찾는다. `vim.fs.root`는 "가장 가까운" 조상을 돌려주기 때문에, 멀티모듈에서 모듈의
`build.gradle`을 먼저 보면 프로젝트가 쪼개진다. 그래서 프로젝트 전체를 뜻하는 표식을 1순위로 둔다.

1. `settings.gradle(.kts)` / `gradlew` / `mvnw`
2. `pom.xml` / `build.gradle(.kts)`
3. `.git`
4. 그래도 없으면 파일이 있는 폴더 (연습용 단일 파일 모드)

워크스페이스는 `~/.cache/nvim/jdtls-workspaces/<루트경로를_밑줄로_바꾼_이름>`에 만든다. 이름이 같은 프로젝트가 여럿이어도 섞이지 않는다.

정해 둔 것들:

- **포맷은 jdtls가 하지 않는다** (`format.enabled = false`). google-java-format(conform)이 단독으로 책임진다. 저장 타임아웃은 자바만 3초 — JVM을 새로 띄우느라 1초로는 모자란다.
- **import를 `*`로 접지 않는다** (`starThreshold = 9999`). 파일만 보고 무엇을 쓰는지 알기 위해서.
- **완성으로 클래스를 고르면 import가 자동으로 붙는다** (`resolveAdditionalTextEditsSupport`). 이게 빠지면 매번 손으로 import를 쓴다.
- **인레이 힌트는 기본 on**. 자바는 타입 이름이 길어 이득이 크다. 끄려면 `<leader>ch`.
- 디버그·테스트 번들은 mason의 `java-debug-adapter`·`java-test`에서 가져오되, `com.microsoft.java.test.runner-jar-with-dependencies.jar`와 `jacocoagent.jar`는 제외한다(공식 README 지시).
- 디버그 중 코드를 고치면 다시 띄우지 않고 반영한다(`hotcodereplace = "auto"`).

## Mermaid

ERD·시퀀스·클래스 다이어그램의 정본 표기법은 Mermaid다. 이유는 렌더러가 이미 세 곳에 있어서다.

- Obsidian: ```` ```mermaid ```` 블록을 그대로 그린다
- GitHub: 마크다운 안에서 그대로 그린다
- 여기: `<leader>mt`(markdown-preview)가 브라우저에서 그린다

treesitter에 `mermaid` 파서가 들어 있어 편집 중에도 문법 색이 붙는다. 별도 CLI나 이미지 변환 단계가 없다.

## 에이전트와 같이 쓰기

특정 벤더 전용 플러그인을 넣지 않았다. 여러 CLI(Claude·Codex·Gemini)를 오가기 때문이다. 대신 범용 패턴을 쓴다.

1. `<leader>tt`로 터미널을 띄우고 에이전트 CLI를 그 안에서 돌린다. 같은 터미널을 dev 서버·`gradlew`와 공유한다.
2. 에이전트가 고친 결과는 `<leader>gd`(diffview)로 파일 단위로 읽는다.
3. 받아들일 헝크만 `<leader>hs`로 스테이징하고 나머지는 `<leader>hr`로 되돌린다.
4. 커밋은 `<leader>lg`(lazygit)에서 묶는다.

에이전트 통합 플러그인은 범용 표준(ACP)의 nvim 클라이언트가 성숙하면 다시 본다.

## 문서 산출물

이 설정은 마크다운 편집까지만 맡는다. 변환은 CLI 몫이다.

| 목적 | 도구 |
| --- | --- |
| PDF | Typst 또는 pandoc |
| 슬라이드 | Marp 또는 Slidev |
| 다이어그램 | Mermaid (위 참고) |
| 블로그 원고 | `fm` 스니펫으로 front-matter 생성 → mdx |

## 알아둘 것

- **첫 파서를 받은 직후**에는 이미 열려 있던 버퍼에 하이라이팅이 안 붙어 있을 수 있다. `:e`로 다시 읽으면 된다.
- **Spring 프로젝트의 첫 인덱싱은 수십 초 걸린다.** 그동안 완성이 비어 보이는 건 정상이다. 상태는 하단에 뜬다.
- **JDK를 올리면** `ftplugin/java.lua`의 폴백 경로(`temurin-21.0.9`)와 `runtimes`의 `JavaSE-21`을 같이 고쳐야 한다. `JAVA_HOME`이 잡혀 있으면 그쪽이 우선이라 대개는 문제되지 않는다.
- **Android는 편집용으로만 쓴다.** jdtls는 Android Gradle Plugin을 안정적으로 읽지 못한다. 빌드·디버그·에뮬레이터는 Android Studio(+IdeaVim)에서 한다. 여기서 되는 건 코드 읽기·이동·리팩터링 정도다.
- **PostgreSQL 콘솔(`:DBUI`)은 `psql`이 있어야 접속된다.** `brew install libpq` 후 PATH에 붙이면 된다. 플러그인 자체는 그것 없이도 설치돼 있다.
- **일간 노트는 `yggdrasil/2-me/dairy/1. 일간`에 `YYYY-MM-DD`로 만든다.** 볼트의 기존 파일을 보고 맞춘 값이라, 다른 폴더를 쓰고 있었다면 `plugins/editor/obsidian.lua`에서 고친다.
- **treesitter 파서 컴파일에는 `tree-sitter` CLI가 필요하다.** Homebrew에서는 `tree-sitter`가 아니라 **`tree-sitter-cli`** 포뮬러다(`tree-sitter`는 C 라이브러리만 깐다).

## 문제가 생기면

| 증상 | 확인할 곳 |
| --- | --- |
| 하이라이팅이 없다 | `:checkhealth nvim-treesitter` — CLI와 파서 설치 여부 |
| 완성이 안 뜬다 | `:checkhealth blink` |
| LSP가 안 붙는다 | `:LspInfo`, 그다음 `:Mason`에서 서버 설치 여부 |
| 자바가 이상하다 | `:LspInfo`로 root_dir 확인 → 워크스페이스(`~/.cache/nvim/jdtls-workspaces/`) 해당 폴더를 지우고 다시 열기 |
| 플러그인 상태 | `:Lazy` |

설정 전체를 되돌리려면 `git checkout main` — 이전 설정이 그대로 있다.
