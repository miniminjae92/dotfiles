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
* **Command Line Tools**:
    * `zoxide` for smarter directory navigation (`z` replaces `cd`).
    * `eza` as a modern `ls` replacement (with icons).
    * `bat` for file viewing with syntax highlighting (replaces `cat`).
    * `fzf` with `fd` for fast and efficient file and directory searching.
    * `gh` for GitHub CLI workflows.
    * `thefuck` to correct command typos.
* **Local Scripts**:
    * `bin/prfb` exports GitHub PR review feedback to Obsidian Markdown and JSON.
    * `bin/prfbo` opens saved PR feedback through `fzf` and `nvim`.
    * `bin/git-cm-ai` generates AngularJS-style commit message candidates from staged diffs, validates the format, and copies the result to the clipboard. It can be run as `git cm-ai`.
    * `bin/lazygit-ai-commit` is the underlying script used by `git-cm-ai` and lazygit.
    * `bin/vault-ai-classify` creates read-only AI classification reports for the Obsidian vault.
    * `~/.dotfiles/bin` is added to `PATH` by `.zshrc`, so these scripts do not need per-command symlinks in `~/.local/bin`.
* **Tmux**: A terminal multiplexer setup for persistent sessions and pane management.
    * **Plugins**: Uses `tpm` (Tmux Plugin Manager) with `tmux-tokyo-night` for status bar theming, and `tmux-resurrect` and `tmux-continuum` to automatically save and restore sessions.
    * **Integration**: Seamlessly integrates with Neovim using `vim-tmux-navigator`.
* **VSCode**: Configuration files to make VSCode feel more like Neovim.

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
    If a target already exists as a regular file, the installer leaves it alone and reports it.
    To back up those files and restore the symlinks intentionally, run:
    ```bash
    ~/.dotfiles/install.sh --replace
    ```
    `.zshrc` adds `~/.dotfiles/bin` to `PATH`, so local scripts are available directly after opening a new shell:
    ```bash
    command -v git-cm-ai
    command -v prfb
    command -v prfbo
    ```

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
        brew install eza bat fzf fd gh thefuck zoxide pyenv lazygit ollama jq
        ```

    * **Install an optional local commit-message model:**
        ```bash
        ollama serve
        ollama pull qwen2.5-coder:7b
        ```
        Stage files or hunks, then run `git cm-ai` to choose an AI provider and copy an AngularJS-style commit message candidate. Paste it into your commit prompt and review it before committing.

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
* **Vim Integration**: `<C-h>`, `<C-j>`, `<C-k>`, `<C-l>` to navigate between Vim/Neovim splits and tmux panes.
