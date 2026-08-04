### macOS Dotfiles

This repository contains my personal dotfiles for macOS, designed to create a streamlined and productive development environment. The setup focuses on a minimalist terminal experience with a powerful Neovim configuration.

#### Features

* **Terminal & Zsh**
    * **iTerm2 Theme**: Uses the [Catppuccin Mocha](https://github.com/catppuccin/iterm) color scheme.
    * **Shell**: A plain `.zshrc` with no framework. Every component is a Homebrew formula sourced directly.
    * **Prompt**: `Starship` under Ghostty, `Powerlevel10k` elsewhere, selected by `$TERM_PROGRAM`.
    * **Plugins**: `zsh-syntax-highlighting` (command validation) and `zsh-autosuggestions` (history-based completion).
    * **Git abbreviations**: `.config/zsh/git.zsh` — Oh My Zsh naming, no Oh My Zsh.
* **Neovim**: A robust Neovim setup managed by `lazy.nvim`.
    * **Theming**: Uses `solarized-osaka.nvim` for a clean, dark color scheme.
    * **Keymaps**: A consistent keybinding system with `<leader>` set to `space`, for easy navigation, window management, and text manipulation.
    * **LSP & Completion**: Uses Neovim's native LSP (`lsp/` directory + `vim.lsp.enable`), with `mason.nvim` supplying the servers and `nvim-lspconfig` acting purely as a defaults database. Java runs through `nvim-jdtls` from `ftplugin/java.lua`. Autocompletion is handled by `blink.cmp`.
    * **Configuration Context**: See `.config/nvim/README.md` before changing the Neovim setup; update it whenever the structure, plugins, keymaps, or tooling instructions change.
* **Command Line Tools**:
    * `zoxide` for smarter directory navigation (`z` replaces `cd`).
    * `eza` as a modern `ls` replacement (with icons).
    * `bat` for file viewing with syntax highlighting (replaces `cat`), including the `tokyonight_night` theme.
    * `fzf` with `fd` for fast and efficient file and directory searching.
    * `gh` for GitHub CLI workflows.
* **Local Scripts**:
    * `bin/prfb` exports GitHub PR review feedback to Obsidian Markdown and JSON.
    * `bin/prfbo` opens saved PR feedback through `fzf` and `nvim`.
    * `git-ai-commit` (AI commit suite: plan/apply/message + lazygit integration) now lives in its own repository — see Extracted Tools below. `bin/git-cm-ai` stays as a thin compatibility wrapper.
    * `agent-notify` (provider-neutral persistent notifications + menu bar app) now lives in its own repository — see Extracted Tools below. Hook wiring and the two LaunchAgents stay here.
    * `codex-accounts` (isolated per-account Codex homes + no-turn quota monitoring: `gcodex`/`ncodex`/`codex-account-usage`) now lives in its own repository — see Extracted Tools below.
    * `bin/personal-ops` creates a weekly Obsidian review and performs a quiet, read-only Mac security check. Slack receives only a completion/deviation notice with an Obsidian link.
    * `bin/ai-model-status` shows centrally configured models and checks provider installation and login state without inference by default.
    * `kman` (Korean man pages, on-device translation) now lives in its own repository — see Extracted Tools below.
    * `video-summary` (YouTube transcript capture, opt-in summaries) now lives in its own repository — see Extracted Tools below. Agent sessions use the `vsummary` skill for batch procedures.
    * `mdview` (local Markdown reader site) now lives in its own repository — see Extracted Tools below.
    * `bin/vault-ai-classify` creates read-only AI classification reports for the Obsidian vault.
    * `bin/zcp` and `bin/zmv` copy or move files into a directory selected with `zoxide query -i`.
    * Local scripts are linked into `~/.local/bin` by `install.sh`.
* **Conventions**: Commit-message conventions are stored under `conventions/` and linked into `~/.config/commit-message-conventions/`. Korean AngularJS is the default, and the original English AngularJS convention is kept as an alternative.
* **Tmux**: A terminal multiplexer setup for persistent sessions and pane management.
    * **Plugins**: Uses `tpm` (Tmux Plugin Manager) with `tmux-tokyo-night` for status bar theming, and `tmux-resurrect` and `tmux-continuum` to automatically save and restore sessions.
    * **Integration**: Seamlessly integrates with Neovim using `vim-tmux-navigator`.
* **VSCode**: Configuration files to make VSCode feel more like Neovim.
* **Agent CLI notifications**: Global Codex, `agy`, and Claude Code `Stop` hooks call `agent-notify`, so completion notifications do not depend on terminal or tmux focus. Codex `PermissionRequest` and Claude Code `Notification` events report permission prompts and idle waits as attention-level alerts. `alerter` provides actionable alerts and click-to-focus navigation to the recorded tmux window and pane. Local presentation and Slack delivery are independent policies, and unacknowledged events can use delayed Slack fallback. Prompts, responses, model names, and detailed errors are excluded from notification state. The tool and its design record live in the agent-notify repository (Extracted Tools below); this repository keeps the hook wiring and LaunchAgents.
* **Shared agent instructions**: `agents/AGENTS.md` is the provider-neutral instruction core (hard cap 50 lines; conditional workflows live in skills). Codex reads it via the `~/.codex/AGENTS.md` symlink and Gemini/agy via `~/.gemini/GEMINI.md`. AGY stores its OAuth session in one macOS Keychain item; use `agy` directly. `agents/routing.json` declares model and account routing as logical roles (planner/worker/reviewer/mechanical); it is a human-facing registry checked for drift by tooling, not an automatic router. `agents/skills/` holds provider-neutral skills (`developer-agent-os`, `handoff-session`, the vendored Matt Pocock engineering chain) linked into both `~/.codex/skills/` and `~/.claude/skills/`, while Codex-specific skills stay under `agents/codex/skills/`. `handoff-session` writes the compact continuation note that carries work context across sessions, providers, and machines.
* **Claude Code**: `claude/CLAUDE.md` is linked to `~/.claude/CLAUDE.md` and imports the shared agent instructions with an `@` import, keeping a thin Claude-specific section (model routing defaults) below the neutral core. Managed settings (`claude/settings-fragment.json`: hooks and the status line) are merged into the machine-local `~/.claude/settings.json` by `install.sh` because Claude Code rewrites that file at runtime; only missing keys and hook events are added, and existing entries are never overwritten. The status line (`bin/claude-statusline`) shows directory, model, and context-window usage as an always-on gauge for judging handoff timing, and a `PreCompact` hook raises an attention alert when auto-compaction is imminent — the signal that a handoff point was missed.
* **Codex**: Global Codex instructions, lifecycle hooks, custom agents, and custom skills are managed through symlinks under `~/.codex/`. `~/.codex/config.toml` stays local because it contains machine-specific project trust state. The local sandbox policy uses `workspace-write` with broad personal work roots (`~/.dotfiles`, `~/.obsidian`, `~/projects`, common document folders, and the iCloud Obsidian vault) plus `on-request` approval for protected or exceptional paths, so normal work proceeds without exposing the entire home directory. The global Codex hook source lives at `agents/codex/hooks.json`.

---

### Installation

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:miniminjae92/dotfiles.git ~/.dotfiles
    ```

2.  **Backup existing files**
    ```bash
    # You can move them to a different directory or add a .bak extension
    mv ~/.gitconfig ~/.gitconfig.bak
    mv ~/.zshrc ~/.zshrc.bak
    mv ~/.tmux.conf ~/.tmux.conf.bak
    mv ~/.vimrc ~/.vimrc.bak
    mv ~/.config/nvim ~/.config/nvim.bak
    ```

3.  **Install Homebrew packages**
    ```bash
    brew bundle --file ~/.dotfiles/Brewfile
    ```
    The Brewfile is the single definition of required CLI tools and casks.

    This step comes **before** `install.sh`, not after. `install.sh` finishes by
    rebuilding the `bat` cache, and `.zshrc` sources Starship, Powerlevel10k,
    `zsh-autosuggestions`, and `zsh-syntax-highlighting` from the Homebrew prefix.
    None of that exists yet on a fresh machine.

4.  **Create symbolic links**
    ```bash
    ~/.dotfiles/install.sh
    ```
    `install.sh` links local scripts into `~/.local/bin`, so they are available directly after opening a new shell:
    ```bash
    command -v git-cm-ai
    command -v personal-ops
    command -v ai-model-status
    command -v prfb
    command -v prfbo
    ```
    Codex, `agy`, and Claude Code completion notifications are enabled by the global hook links installed by this script. The `agent-notify` tool itself lives in its own repository (see Extracted Tools below) and is linked only when the clone exists.

    The install script links only stable Codex instructions, hooks, custom agents, and custom skills. It does not manage Codex config, auth, logs, sessions, caches, system skills, or local state.
    It also links the managed `bat` theme into `~/.config/bat/themes/` and rebuilds the `bat` cache.
    Codex helper commands become available after opening a new shell:
    ```bash
    agent-os-usage               # 현재 Codex 세션(정확한 thread id)
    agent-os-usage --latest      # 명시적으로 가장 최근 캡처
    ```
    `agent-os-usage` reports the current Codex thread only when `CODEX_THREAD_ID` matches captured events.
    It never substitutes another provider/session; use `--latest` only when that fallback is intentional.
    Claude usage is reported unavailable until its Stop hook emits the same usage schema.
    These token counts are not ChatGPT credits or API cost.
    Two-account Codex work (`gcodex`/`ncodex` isolated homes, no-turn quota
    monitoring, threshold/collision warnings) is documented in the
    [codex-accounts repository](https://github.com/miniminjae92/codex-accounts).
    Per-machine facts that stay true here: each `auth.json` under
    `~/.codex-accounts/` is local credential state (mode 600, never commit),
    and the `com.miniminjae.codex-account-usage` LaunchAgent runs the monitor
    at 09:00 and every 15 minutes.
    AI model names are managed in `ai-tools/models.json`, linked to `~/.config/ai-tools/models.json`. The registry contains task assignments and model names only, never credentials. Existing model environment variables remain temporary overrides, and `ai-model-status` reports the effective override when one is set.

5.  **Verify the installation**
    ```bash
    dotfiles-doctor
    ```
    Read-only health check over symlinks, required tools, agent CLI auth, launchd
    jobs, and model-registry drift. It never changes state; the exit code is the
    number of `FAIL` findings. `WARN` lines are usually the per-machine steps in
    step 6 that have not been done yet.

    `install.sh` prints its own failure report at the end — skipped symlinks and
    LaunchAgents that would not load. An empty report plus `Installed dotfile links.`
    is what a clean run looks like.

6.  **Per-machine setup that no script performs**

    * **Shell environment.** Oh My Zsh is **not** used and must not be installed.
        It was removed in favour of Starship (Ghostty) and Powerlevel10k (iTerm2),
        selected at runtime by `$TERM_PROGRAM`. The prompt, `zsh-autosuggestions`,
        and `zsh-syntax-highlighting` all come from the Brewfile in step 3. Git
        abbreviations live in `.config/zsh/git.zsh`, which keeps the Oh My Zsh
        naming convention without depending on Oh My Zsh.

    * **Powerlevel10k configuration.** `~/.p10k.zsh` is machine-local and not in
        this repository. Run `p10k configure` once, or copy the file across.

    * **fzf-git keybindings.** `.zshrc` sources `~/fzf-git.sh/fzf-git.sh`:
        ```bash
        git clone https://github.com/junegunn/fzf-git.sh.git ~/fzf-git.sh
        ```

    * **Obsidian vaults.** Nothing bootstraps these. `agent-os/paths.env` is the
        contract: `YGGDRASIL_VAULT=$HOME/.obsidian/yggdrasil` and
        `DEVELOPER_OS_VAULT=$HOME/.obsidian/mimir`. Restore both vaults at those
        paths, or override the variables. A skeleton for a new vault is in
        `agent-os/vault-template/`.

    * **Secrets.** Nothing secret is in this repository, so nothing secret is
        restored by it: `~/.gemini.env`, the Slack webhook and `agy` session in the
        macOS Keychain, and `~/.codex-accounts/{google,naver}/auth.json` (mode 600)
        are all per-machine.

    * **A different macOS username breaks the LaunchAgents.** Every plist in
        `.config/launchd/` hardcodes `/Users/miniminjae/…`. On a machine with
        another username they load and then fail silently. Rewrite the paths first.

    Notification behavior — delivery axes, named modes, the menu bar app,
    `AGENT_NOTIFY_POLICY` process-tree scoping, and ownership-based `alerter`
    reclamation (the 83 GB incident) — is documented in the
    [agent-notify repository](https://github.com/miniminjae92/agent-notify).
    What stays per-machine here: install.sh links the hooks and the two
    LaunchAgents (`agent-notify-sweep`, `agent-notify-menu`) and builds
    `~/Applications/AgentNotifyMenu.app` from the clone when it exists. Codex
    `PermissionRequest` hooks create priority attention events without storing
    the requested command or tool input; after changing the hook file, open
    `/hooks` once in Codex to review and trust the new hook hash. Slack
    escalation is per-machine Keychain state — the webhook URL never lands in
    this repository:

    ```bash
    agent-notify slack configure          # agent 작업 알림 채널
    agent-notify slack configure usage    # 계정 사용량 별도 채널
    agent-notify slack test
    ```

    Idle resources are reclaimed by background jobs instead of by remembering to clean up.
    `agent-notify sweep` runs every minute: it acknowledges pending events older than
    `pending_ttl_days`, projects the pending count to `pending.json` so the statusline can
    warn once it passes ten, and reclaims any `alerter` that outlived its worker. Events
    with both local and Slack delivery off are acknowledged the moment they are presented —
    nothing will ever reach the user, so leaving them pending only grows a queue no click
    can drain. Reclamation is scoped by ownership: only PIDs that `agent-notify` recorded
    when spawning are eligible, and the executable path is re-checked immediately before
    signalling, so a recycled PID or another tool's same-named process is never killed.
    `persistent_seconds`, `temporary_seconds`, and `pending_ttl_days` live in
    `.config/agent-notify/config.json`.

    `simulator-reaper` (its own repository — see Extracted Tools below) runs every
    ten minutes via the `com.miniminjae.simulator-reaper` LaunchAgent and reclaims
    booted iOS simulators that survive Xcode — never while any dev tool is running.

    Personal operations run quietly in the background. The security job runs daily at
    10:00, establishes an external-listener baseline on its first run, and sends Slack only
    for new, changed, resolved, or failed checks. It inspects SIP, Gatekeeper, FileVault,
    the firewall, Codex auth-file permissions, recommended macOS updates, and new external
    TCP listeners; it never changes those settings. The weekly job runs Sunday at 21:00,
    asks Codex at low reasoning effort to summarize the last seven days of Developer OS
    Runs/Reviews and dotfiles commit subjects, writes the review under Obsidian's
    `AI Work Reports/Weekly Reviews`, then sends only an Obsidian link to Slack. It falls
    back to a rules-only draft if Codex is unavailable.

    ```sh
    personal-ops security
    personal-ops weekly
    personal-ops weekly --no-agent
    ```
    Normal completions escalate after 10 minutes without acknowledgement; attention and error events escalate after 3 minutes. Disable external delivery without deleting the Keychain item with `agent-notify slack disable`.

    When leaving the Mac after starting an agent task, enable immediate mobile delivery for the next result or for a bounded period:
    ```bash
    agent-notify away once
    agent-notify away on
    agent-notify away on --for 2h
    agent-notify away status
    agent-notify away off
    ```
    `away once` is consumed by the next normalized agent event. `away on` remains active until it is disabled, while `--for` accepts minute, hour, or day durations such as `30m`, `2h`, or `1d` up to 30 days. Away events are sent by the background worker immediately and retain the normal sweep retry path. Configure the Slack iOS destination channel for every new message and mobile delivery immediately, even while the desktop is active.

    * **Install an optional local commit-message model:**
        ```bash
        ollama serve
        ollama pull qwen2.5-coder:7b
        ```
        Stage files or hunks, then run `git ai-commit message` to choose an AI provider and copy a Korean AngularJS-style commit message candidate. Every provider uses a compact diff prompt by default; pass `--full` for more context or set `LAZYGIT_AI_COMMIT_CODEX_MODEL=gpt-5.5` for harder Codex changes. The older `git cm-ai` entry point remains compatible.

7.  **Install iTerm2 Theme**
    * Download the `Catppuccin Mocha.itermcolors` file from the [official repository](https://github.com/catppuccin/iterm/blob/main/colors/catppuccin-mocha.itermcolors).
    * In iTerm2, go to **Preferences (`Cmd + ,`) > Profiles > Colors**.
    * Click **Color Presets... > Import...** and select the downloaded file.
    * Select `Catppuccin Mocha` from the `Color Presets...` list to apply.

8.  **Install Neovim plugins**
    * Open Neovim (`nvim`).
    * Run `:Lazy` to install all plugins listed in the config.
    * Run `:MasonInstallAll` to install all the LSP servers, linters, formatters, and debuggers.

9.  **Setup VSCode (Optional)**
    * Follow the instructions in the `vscode/README.md` to create symbolic links for your VSCode settings and keybindings.

---

### Repository Layout

의미 규칙 한 줄: **`agents/`는 설비 세팅값(고치면 에이전트가 다르게 일함, 전부 홈으로 설치됨), `agent-os/`는 운전 일지·계측 규격서(고쳐도 에이전트는 그대로, 홈 링크 0)**. 용어는 [CONTEXT.md](CONTEXT.md), 결정 배경은 `agent-os/DECISIONS.md` D-014.

| 디렉터리 | 정체 | install.sh 링크 |
| --- | --- | --- |
| `agents/` | 에이전트가 읽는 실행 자산 전부 | 아래 전부 |
| `agents/AGENTS.md` | 공급자 중립 공통 지침 | `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md` |
| `agents/routing.json` + `models.json` | 라우팅 패키지 (역할→모델, 정형 태스크) | models.json → `~/.config/ai-tools/` |
| `agents/skills/` | 스킬 — 자작 + 벤더(각 VENDOR.md, 대장: `agent-os/upstreams.md`) | `~/.claude/skills/*`, `~/.codex/skills/*` |
| `agents/conventions/` | 커밋 메시지 규약 | `~/.config/commit-message-conventions/` |
| `agents/claude/` | Claude 어댑터 (CLAUDE.md, settings 병합 조각) | `~/.claude/CLAUDE.md` |
| `agents/codex/` | Codex 어댑터 (~/.codex 미러: hooks, agents toml, 전용 스킬) | `~/.codex/{hooks.json,agents,skills}` |
| `agents/gemini/` | Gemini 어댑터 (알림 훅) | `~/.gemini/config/hooks.json` |
| `agent-os/` | 운영 결정(DECISIONS)·상태·계약(paths.env)·상류 대장(upstreams) | 없음 — 불변식 |
| `bin/` | CLI 도구 전부 | `~/.local/bin/*` |
| `man/` `style/` `tests/` `vscode/` | 에이전트와 무관한 일반 dotfiles 자산 | 일부 |

---

### Extracted Tools

실질 도구는 독립 저장소로 이관했다(D-022). install.sh가 `~/projects/<repo>`
클론이 있으면 `~/.local/bin`으로 링크하고, 없으면 건너뛴다:

- **agent-notify** — 에이전트 CLI 공용 영속 알림(+메뉴 막대 앱). 소유권 기반 alerter 회수(D-016)·pending과 배너 수명 분리(D-017) — <https://github.com/miniminjae92/agent-notify>. 훅 배선·LaunchAgent 2종·개인 config는 이 레포에 남고, install.sh가 클론에서 메뉴 앱을 빌드한다
- **asx** — 에이전트 세션 통합 탐색기(Claude 본대화·서브에이전트·다계정 Codex·기기 미러) — <https://github.com/miniminjae92/asx>
- **codex-accounts** — 계정 격리 Codex 홈 + MCP 무턴 쿼터 감시(gcodex·ncodex·codex-account-usage) — <https://github.com/miniminjae92/codex-accounts>. LaunchAgent와 auth.json 600 규약은 이 레포에 남는다
- **simulator-reaper** — 유휴 iOS 시뮬레이터 회수(가드·유예·dry-run) — <https://github.com/miniminjae92/simulator-reaper>. LaunchAgent는 이 레포에 남는다
- **kman** — 한국어 man 페이지 (Apple 온디바이스 번역·용어집·캐시) — <https://github.com/miniminjae92/kman>
- **mdview** — 마크다운 디렉터리 로컬 리더 — <https://github.com/miniminjae92/mdview>
- **video-summary** — 유튜브 전사 저장(기본 무모델)·옵트인 요약·채널 배치 — <https://github.com/miniminjae92/video-summary>. 에이전트 세션에서는 `vsummary` 스킬이 배치 절차를 안내한다. 노트 저장 위치는 `.zshrc`의 `VIDEO_SUMMARY_DIR`가 vault로 지정
- **git-ai-commit** — AI 커밋 스위트(plan/apply/message + lazygit 연동 + man 페이지) — <https://github.com/miniminjae92/git-ai-commit>. `git cm-ai`·`git plan-ai` 호환 명령은 유지되고, 모델 라우팅은 `~/.config/ai-tools/models.json`(install.sh가 `agents/models.json`을 링크)

---

### AI Model Status

Configured model names and non-inference provider status:

```bash
ai-model-status
ai-model-status --json
```

Run minimal live inference only when model availability must be verified. This uses a small amount of the selected provider's model tokens or credits:

```bash
ai-model-status --probe agy
ai-model-status --probe codex
```

---

### Keybindings

#### Neovim

* **Leader Key:** `<Space>`
* **Window Management**
    * `<leader>sv`: Split vertically
    * `<leader>sh`: Split horizontally
    * `<leader>se`: Make splits equal size
    * `<leader>sx`: Close current split
    * `<leader>sm`: Maximize/minimize split
* **File Explorer**: `<leader>ee` toggles the `snacks.nvim` tree; `-` opens the current folder in `oil.nvim` for editing.
* **Fuzzy Finding** (`fzf-lua`):
    * `<leader>ff`: Find files
    * `<leader>fs`: Live grep string

> The full keymap table and the reasoning behind each layer live in `.config/nvim/README.md`.

#### Tmux

* **Prefix**: `<C-a>`
* **Splitting Panes**
    * `|`: Split vertically
    * `-`: Split horizontally
* **Resizing Panes**: Use prefix + `h`, `j`, `k`, `l` to resize panes. `m` to maximize/minimize.
* **Reordering Windows**: Use prefix + `Shift+Left` or `Shift+Right` to swap the current window with its neighbor.
* **Clipboard Cleanup**: Use prefix + `T` to trim leading/trailing whitespace from each clipboard line with `cleanclip trim` (installed from `bin/`).
* **Vim Integration**: `<C-h>`, `<C-j>`, `<C-k>`, `<C-l>` to navigate between Vim/Neovim splits and tmux panes.
