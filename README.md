### macOS Dotfiles

This repository contains my personal dotfiles for macOS, designed to create a streamlined and productive development environment. The setup focuses on a minimalist terminal experience with a powerful Neovim configuration.

#### Features

* **Terminal & Zsh**
    * **iTerm2 Theme**: Uses the [Catppuccin Mocha](https://github.com/catppuccin/iterm) color scheme.
    * **Shell**: Managed by `Oh My Zsh`.
    * **Prompt**: Styled with `Powerlevel10k`.
    * **Plugins**: `zsh-syntax-highlighting` (command validation) and `zsh-autosuggestions` (history-based completion).
* **Neovim**: A robust Neovim setup managed by `lazy.nvim`.
    * **Theming**: Uses `solarized-osaka.nvim` for a clean, dark color scheme.
    * **Keymaps**: A consistent keybinding system with `<leader>` set to `space`, for easy navigation, window management, and text manipulation.
    * **LSP & Completion**: Integrates `mason.nvim` and `nvim-lspconfig` for language server protocol (LSP) support for languages like C, C++, Java, Svelte, and Python. Autocompletion is handled by `nvim-cmp` with `LuaSnip`.
    * **Configuration Context**: See `.config/nvim/README.md` before changing the Neovim setup; update it whenever the structure, plugins, keymaps, or tooling instructions change.
* **Command Line Tools**:
    * `zoxide` for smarter directory navigation (`z` replaces `cd`).
    * `eza` as a modern `ls` replacement (with icons).
    * `bat` for file viewing with syntax highlighting (replaces `cat`), including the `tokyonight_night` theme.
    * `fzf` with `fd` for fast and efficient file and directory searching.
    * `gh` for GitHub CLI workflows.
    * `thefuck` to correct command typos.
* **Local Scripts**:
    * `bin/prfb` exports GitHub PR review feedback to Obsidian Markdown and JSON.
    * `bin/prfbo` opens saved PR feedback through `fzf` and `nvim`.
    * `bin/git-ai-commit` is the unified entry point for AI-assisted commit planning, applying a cached plan, and staged-change message generation. It can be run as `git ai-commit`.
    * `bin/git-cm-ai` and `bin/git-plan-ai` remain available as compatibility commands for message-only and plan-only workflows.
    * `bin/agent-notify` provides provider-neutral, metadata-only completion alerts for agent CLIs. Codex and `agy` adapters are included, and future CLIs can emit normalized events without changing the notification or Slack logic.
    * `bin/gcodex` and `bin/ncodex` run Codex with isolated Google/Naver account homes and file-based authentication scoped to each account home.
    * `bin/codex-account-usage` reads account usage and reset windows without starting a model turn, and reports daily or threshold changes through `agent-notify` and Slack.
    * `bin/personal-ops` creates a weekly Obsidian review and performs a quiet, read-only Mac security check. Slack receives only a completion/deviation notice with an Obsidian link.
    * `bin/lazygit-ai-commit` is the underlying message generator used by `git ai-commit message`, `git-cm-ai`, and lazygit.
    * `bin/ai-model-status` shows centrally configured models and checks provider installation and login state without inference by default.
    * `bin/kman` displays cached Korean man-page translations using Apple's on-device Translation framework and tracks previously unknown abbreviations separately from the translated body.
    * `bin/video-summary` saves a YouTube video's dynamically sized Korean summary with timestamp links as an Obsidian Markdown note. It reuses unchanged summaries to avoid duplicate model calls.
    * `.codex/skills/summarize-youtube-playlist` interactively collects a channel, playlist, named Codex account, browser profile, usage ceiling, and Slack preference before running the safe two-video gate and background playlist batch.
    * `bin/vault-ai-classify` creates read-only AI classification reports for the Obsidian vault.
    * `bin/zcp` and `bin/zmv` copy or move files into a directory selected with `zoxide query -i`.
    * Local scripts are linked into `~/.local/bin` by `install.sh`.
* **Conventions**: Commit-message conventions are stored under `conventions/` and linked into `~/.config/commit-message-conventions/`. Korean AngularJS is the default, and the original English AngularJS convention is kept as an alternative.
* **Tmux**: A terminal multiplexer setup for persistent sessions and pane management.
    * **Plugins**: Uses `tpm` (Tmux Plugin Manager) with `tmux-tokyo-night` for status bar theming, and `tmux-resurrect` and `tmux-continuum` to automatically save and restore sessions.
    * **Integration**: Seamlessly integrates with Neovim using `vim-tmux-navigator`.
* **VSCode**: Configuration files to make VSCode feel more like Neovim.
* **Agent CLI notifications**: Global Codex, `agy`, and Claude Code `Stop` hooks call `agent-notify`, so completion notifications do not depend on terminal or tmux focus. Claude Code additionally reports `Notification` events (permission prompts, idle waits) as attention-level alerts through the same pipeline. `alerter` provides actionable alerts and click-to-focus navigation to the recorded tmux window and pane. Local presentation and Slack delivery are independent policies, and unacknowledged events can use delayed Slack fallback. Prompts, responses, model names, and detailed errors are excluded from notification state.
* **Shared agent instructions**: `agents/AGENTS.md` is the provider-neutral instruction core (hard cap 50 lines; conditional workflows live in skills). Codex reads it via the `~/.codex/AGENTS.md` symlink and Gemini/agy via `~/.gemini/GEMINI.md`; account wrappers (`magy`, `sagy`) share it into each account home. `agents/routing.json` declares model and account routing as logical roles (planner/worker/reviewer/mechanical); it is a human-facing registry checked for drift by tooling, not an automatic router. `agents/skills/` holds provider-neutral skills (`work`, `developer-agent-os`) linked into both `~/.codex/skills/` and `~/.claude/skills/`, while Codex-specific skills stay under `.codex/skills/`.
* **Claude Code**: `claude/CLAUDE.md` is linked to `~/.claude/CLAUDE.md` and imports the shared agent instructions with an `@` import, keeping a thin Claude-specific section (model routing defaults) below the neutral core. Hook configuration is merged into the machine-local `~/.claude/settings.json` by `install.sh` because Claude Code rewrites that file at runtime; only missing hook events are added, and existing entries are never overwritten.
* **Codex**: Global Codex instructions, lifecycle hooks, custom agents, and custom skills are managed through symlinks under `~/.codex/`. `~/.codex/config.toml` stays local because it contains machine-specific project trust state. The global Agent OS hook source lives at `agent-os/hooks.json` so it is not loaded again as a project-local hook while working in this repository.

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

3.  **Create symbolic links**
    ```bash
    ~/.dotfiles/install.sh
    ```
    `install.sh` links local scripts into `~/.local/bin`, so they are available directly after opening a new shell:
    ```bash
    command -v git-cm-ai
    command -v git-plan-ai
    command -v git-ai-commit
    command -v agent-notify
    command -v gcodex
    command -v ncodex
    command -v codex-account-usage
    command -v personal-ops
    command -v ai-model-status
    command -v kman
    command -v prfb
    command -v prfbo
    command -v video-summary
    ```
    Codex and `agy` completion notifications are enabled by the global hook links installed by this script. The provider-neutral entry point for another CLI is:
    ```bash
    agent-notify event --source future-agent --status complete --project example
    ```
    Inspect and handle pending events with:
    ```bash
    agent-notify status
    agent-notify ack <event-id>
    agent-notify ack --all
    agent-notify open <event-id>
    ```
    Verify the basic macOS notification path with `agent-notify test`; macOS may ask for notification permission the first time.

    The install script links only stable Codex instructions, hooks, custom agents, and custom skills. It does not manage Codex config, auth, logs, sessions, caches, system skills, or local state.
    It also links the managed `bat` theme into `~/.config/bat/themes/` and rebuilds the `bat` cache.
    Codex helper commands become available after opening a new shell:
    ```bash
    work "implement the requested change"
    work
    arc
    agent-os-usage
    arc 019e4830
    arc docs/conversation/2026-05-21-agent-session.md
    ```
    `arc` without an argument exports the latest Codex session from `~/.codex/sessions` into `docs/conversation/YYYY-MM-DD-agent-session.md`, then runs the archive workflow. Pass a resume code or session id fragment to archive a specific session.
    `agent-os-usage` reports the latest captured session token totals and the delta since the previous Stop event. These token counts are not ChatGPT credits or API cost.
    `gcodex` and `ncodex` keep authentication, sessions, memories, usage records, and file-based credentials under separate `~/.codex-accounts/google` and `~/.codex-accounts/naver` directories. Shared configuration, hooks, agents, and skills remain linked from `~/.codex`. Each `auth.json` is local credential state and must remain mode 600; never commit or copy it. Authenticate each command once with `gcodex login` and `ncodex login`. On macOS these commands use device authorization and open Chrome's `Default` profile for `gcodex` and `Profile 1` for `ncodex`; override them with `CODEX_GOOGLE_CHROME_PROFILE` or `CODEX_NAVER_CHROME_PROFILE` if Chrome profile directories change. An existing login is left intact; run the matching `logout` command first only when intentionally switching accounts. Plain `codex` remains available but is intentionally excluded from this two-account usage-monitoring workflow; use the named wrappers for managed work so an unrelated default login cannot be mistaken for Google or Naver. Existing legacy Keychain entries are ignored and are not deleted automatically.
    Use `gcodex usage` or `ncodex usage` for an immediate account report; the masked ChatGPT email in the report verifies which account the wrapper actually resolved. A LaunchAgent runs explicitly at 09:00 and every 15 minutes, sends one daily Slack report per account after 09:00, warns when usage crosses 75%, 90%, 95%, or 100%, and reports resets when usage drops by at least 20 percentage points. It also warns when both wrappers resolve to the same ChatGPT email, when an account query fails twice consecutively, or when a failure follows 30 minutes without a successful check. Each account recovers its missed daily report independently. It never falls back to plain `codex`, switches accounts, or consumes a reset credit.
    AI model names are managed in `ai-tools/models.json`, linked to `~/.config/ai-tools/models.json`. The registry contains task assignments and model names only, never credentials. Existing model environment variables remain temporary overrides, and `ai-model-status` reports the effective override when one is set.

4.  **Install Oh My Zsh and Plugins**

    * **Install Oh My Zsh:**
        ```bash
        sh -c "$(curl -fsSL [https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh](https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh))"
        ```
        (If it asks to overwrite `~/.zshrc`, you can say no, as we've already symlinked it.)

    * **Install Powerlevel10k Theme:**
        ```bash
        git clone --depth=1 [https://github.com/romkatv/powerlevel10k.git](https://github.com/romkatv/powerlevel10k.git) ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
        ```

    * **Install Zsh Plugins (for OMZ):**
        ```bash
        git clone [https://github.com/zsh-users/zsh-syntax-highlighting.git](https://github.com/zsh-users/zsh-syntax-highlighting.git) ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
        git clone [https://github.com/zsh-users/zsh-autosuggestions.git](https://github.com/zsh-users/zsh-autosuggestions.git) ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
        ```

    * **Install Other CLI Tools (via Homebrew):**
        ```bash
        brew bundle --file ~/.dotfiles/Brewfile
        ```
        The Brewfile is the single definition of required CLI tools and casks. After
        installing, verify the whole environment (symlinks, tools, agent CLI auth,
        launchd jobs, and model-registry drift) with the read-only health check:
        ```bash
        dotfiles-doctor
        ```

    `alerter` returns the selected action to `agent-notify`. Temporary alerts close automatically after eight seconds; persistent alerts wait for an explicit action. Clicking the alert body or **터미널로 이동** acknowledges the event, selects its recorded tmux client/window/pane, and brings the terminal app forward. **확인** acknowledges without changing focus. **나중에** leaves the event pending, so delayed Slack fallback can still run. AppleScript remains a degraded fallback when `alerter` is unavailable, but its click is owned by Script Editor and cannot focus a tmux pane or acknowledge an event.

    Delivery policies are independent: local delivery is `off`, `temporary`, or `persistent`; Slack delivery is `off`, `delayed`, or `immediate`. Start by adjusting the two axes directly instead of assuming a fixed workflow. Run `agent-notify mode --help` to see every value and example:
    ```bash
    agent-notify mode set --local persistent --slack off
    agent-notify mode set --local temporary --slack off
    agent-notify mode set --local persistent --slack immediate
    agent-notify mode set --local off --slack immediate
    agent-notify mode status
    ```

    The existing `normal`, `watch`, `away`, and `quiet` named modes remain available for compatibility, but direct settings are the recommended discovery path until a stable personal pattern emerges.

    Run the following inside a tmux pane to verify click-to-focus behavior:
    ```bash
    agent-notify test
    ```

    To enable Slack escalation, create an Incoming Webhook and enter it directly into the macOS Keychain prompt. The URL is never stored in dotfiles or printed by `agent-notify`:
    ```bash
    agent-notify slack configure
    agent-notify slack status
    agent-notify slack test
    ```

    Keep account-usage reports in a separate Slack channel by registering that channel's
    Incoming Webhook as the `usage` destination. Agent work alerts continue using the
    existing `agent` destination:

    ```sh
    agent-notify slack configure usage
    agent-notify slack status all
    agent-notify slack test usage
    ```

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

5.  **Install iTerm2 Theme**
    * Download the `Catppuccin Mocha.itermcolors` file from the [official repository](https://github.com/catppuccin/iterm/blob/main/colors/catppuccin-mocha.itermcolors).
    * In iTerm2, go to **Preferences (`Cmd + ,`) > Profiles > Colors**.
    * Click **Color Presets... > Import...** and select the downloaded file.
    * Select `Catppuccin Mocha` from the `Color Presets...` list to apply.

6.  **Install Neovim plugins**
    * Open Neovim (`nvim`).
    * Run `:Lazy` to install all plugins listed in the config.
    * Run `:MasonInstallAll` to install all the LSP servers, linters, formatters, and debuggers.

7.  **Setup VSCode (Optional)**
    * Follow the instructions in the `vscode/README.md` to create symbolic links for your VSCode settings and keybindings.

---

### Korean Man Pages

`kman` keeps the normal `man` command as the English source of truth and creates a
versioned Korean cache using Apple's on-device Translation framework:

```bash
man tmux          # English original
kman tmux         # Korean translation
kman 1 tmux       # Explicit man section
```

The first translation builds a small local Swift helper and can take longer. It
requires macOS 26.4 or later, installed Command Line Tools, and downloaded English
and Korean languages under System Settings > General > Language & Region >
Translation Languages. Later calls reuse the source-hash cache under
`~/Library/Caches/kman/` and make no API calls.

Viewer-only changes reuse the newest completed local translation and never start a
new translation automatically. `--refresh` is the explicit opt-in for rebuilding a
translation. Refreshes use the low-latency on-device strategy and save each
successful paragraph immediately, so an interrupted run resumes only unfinished
paragraphs. A paragraph whose protected command token cannot be restored stays in
English instead of failing the whole page.

The translated body contains no inserted acronym explanations. Reviewed common
terms live in `kman/glossary/common.json`; command-specific reviewed terms can be
added under `kman/glossary/commands/`. Unknown abbreviations remain local review
candidates:

```bash
kman --terms tmux       # Reviewed terms used by this page
kman --new-terms tmux   # Unknown acronym candidates only
kman --refresh tmux     # Rebuild after a glossary or translator change
```

The interactive viewer uses terminal display-width wrapping, highlighted section
and option labels, and a `less` progress prompt. Use `/text` to search, `n`/`N`
for the next/previous match, `g`/`G` for the start/end, and `q` to quit. Pass
`--no-pager` when plain output is needed for a pipe or file.

For permissively licensed pages, create a review-first Markdown artifact for a
future blog pipeline. The export is marked `reviewed: false` and includes the
detected source license notice:

```bash
kman --export ./tmux.1.ko.md tmux
```

Pages with unknown or unsupported redistribution terms remain local and are not
exported.

---

### YouTube Video Summaries

In a Codex session, invoke `$summarize-youtube-playlist` to be prompted for the missing channel, playlist, account, browser profile, usage stop threshold, and Slack preference instead of assembling the flags manually.

`video-summary` uses `yt-dlp` for Korean or English subtitles and the authenticated Codex CLI for structured summarization. Check the transcript size and planned strategy without spending model tokens:

```bash
video-summary 'https://www.youtube.com/watch?v=VIDEO_ID' --dry-run
```

Create the summary:

```bash
video-summary 'https://www.youtube.com/watch?v=VIDEO_ID'
```

After reloading `.zshrc`, the shorter `vsummary` alias runs the same command.

By default, notes are saved under `~/.obsidian/yggdrasil/3. Resource/Video Summaries/`. Each note records the transcript hash, summary version, processing strategy, model, and observed token usage. If the video ID, transcript hash, and summary version are unchanged, the existing note is returned without another model call. Use `--force` only when a fresh summary is intentionally required.

For a channel membership, let `yt-dlp` read the signed-in browser profile directly. The cookie database is read at runtime and is never exported by `video-summary`. Discover member candidates across the Membership and Community tabs and every channel playlist, then verify their availability without fetching subtitles or calling Codex:

```bash
video-summary 'https://www.youtube.com/@CHANNEL' \
  --discover-channel-members \
  --cookies-from-browser 'chrome:Profile 1' \
  --list-only
```

`--discover-channel-members` implies channel and members-only mode. It keeps only entries whose resolved `yt-dlp` availability is `subscriber_only`, defaults to all matching videos, and uses `gpt-5.6-luna` with low reasoning in sequential mode. Detailed summaries preserve substantive claims, evidence, procedures, conditions, examples, numbers, exceptions, warnings, and Q&A. Use `--max-videos N` for a bounded first run. Check transcripts without model calls or note writes, then run the same command without `--dry-run` to create notes:

```bash
video-summary 'https://www.youtube.com/@CHANNEL' \
  --discover-channel-members \
  --cookies-from-browser 'chrome:Profile 1' \
  --codex-command gcodex \
  --max-videos 3 \
  --dry-run
```

Run without `--max-videos` and `--dry-run` to process all verified member videos. Notes are stored once, while generated indexes under `Video Summaries/Playlists/` link them in each YouTube playlist's order. A video present in several playlists is summarized only once. The verified member inventory is cached there too; use `--refresh-inventory` when the channel adds videos. One failed or captionless video is reported in the final JSON without stopping later videos. Existing notes with the same detailed-summary version are skipped unless `--force` is provided, so rerunning the identical command resumes safely. Add `--notify-slack` to send completion or attention-required results through the configured `agent-notify` Slack destination. Browser cookies grant account access: keep this as an interactive personal command, never export a cookie file, and review YouTube's current terms before automated use.

---

### AI-assisted Git Commits

Use one command namespace for the complete workflow. With no subcommand it generates a read-only plan, saves it inside `.git/ai-commit-plan.json`, and sends at most 6,000 tracked-diff characters to the Gemini model selected in `agy`. Untracked file contents are never sent:

```bash
git ai-commit
```

Use more tracked diff only when the compact plan lacks context:

```bash
git ai-commit --full
```

Preview the saved plan without changing Git state, then explicitly apply it:

```bash
git ai-commit apply --dry-run
git ai-commit apply
```

`apply` verifies that the repository and working-tree fingerprint still match the saved plan, checks the exact staged paths before every commit, and never pushes. `apply --dry-run` prints the cached commit list and warnings without a model call or Git write. Plans containing warnings stop by default; after human or agent review, confirm the review explicitly with `git ai-commit apply --reviewed`.

Git handles a top-level `--help` as a man-page request before an external command runs. Use either of these forms for the built-in workflow help:

```bash
git ai-commit -h
git ai-commit help
git ai-commit apply --help
```

The dotfiles `MANPATH` includes the bundled `git-ai-commit(1)` page, so after opening a new shell the standard `git ai-commit --help` form works as well.

The plan assigns every changed path exactly once. Sensitive-looking paths such as `.env`, private keys, and credential JSON files stop cloud delegation before `agy` is called. Existing staged paths are accepted only when all of them belong to the first planned commit.

For a manually staged change, generate only a commit message. Compact mode is also the default here:

```bash
git ai-commit message agy
git ai-commit message agy --full
```

The existing `git plan-ai` and `git cm-ai` commands remain available for compatibility.

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
* **File Explorer**: `<leader>ee` to toggle `nvim-tree`.
* **Fuzzy Finding**:
    * `<leader>ff`: Find files
    * `<leader>fs`: Live grep string

#### Tmux

* **Prefix**: `<C-a>`
* **Splitting Panes**
    * `|`: Split vertically
    * `-`: Split horizontally
* **Resizing Panes**: Use prefix + `h`, `j`, `k`, `l` to resize panes. `m` to maximize/minimize.
* **Reordering Windows**: Use prefix + `Shift+Left` or `Shift+Right` to swap the current window with its neighbor.
* **Clipboard Cleanup**: Use prefix + `T` to trim leading/trailing whitespace from each clipboard line with `scripts/cleanclip trim`.
* **Vim Integration**: `<C-h>`, `<C-j>`, `<C-k>`, `<C-l>` to navigate between Vim/Neovim splits and tmux panes.
