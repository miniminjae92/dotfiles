### macOS Dotfiles

This repository contains my personal dotfiles for macOS, designed to create a streamlined and productive development environment. The setup focuses on a minimalist terminal experience with a powerful Neovim configuration.

#### Features

* **Neovim**: A robust Neovim setup managed by `lazy.nvim`.
    * **Theming**: Uses `solarized-osaka.nvim` for a clean, dark color scheme.
    * **Keymaps**: A consistent keybinding system with `<leader>` set to `space`, for easy navigation, window management, and text manipulation.
    * **LSP & Completion**: Integrates `mason.nvim` and `nvim-lspconfig` for language server protocol (LSP) support for languages like C, C++, Java, Svelte, and Python. Autocompletion is handled by `nvim-cmp` with `LuaSnip`.
    * **Zsh**: My shell configuration uses `powerlevel10k` with a custom theme and various useful tools.
    * **Command Line Tools**: `zoxide` for smarter directory navigation, `eza` as a modern `ls` replacement, `bat` for file viewing, and `thefuck` to correct command typos.
    * **Fuzzy Finding**: Utilizes `fzf` with `fd` for fast and efficient file and directory searching.
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
    ln -s ~/.dotfiles/.gitconfig ~/.gitconfig
    ln -s ~/.dotfiles/.gitignore ~/.gitignore
    ln -s ~/.dotfiles/.vimrc ~/.vimrc
    ln -s ~/.dotfiles/.zshrc ~/.zshrc
    ln -s ~/.dotfiles/.config/nvim ~/.config/nvim
    ln -s ~/.dotfiles/.tmux.conf ~/.tmux.conf
    ln -sf ~/.dotfiles/.gitignore ~/.gitignore_global
    git config --global core.excludesFile ~/.gitignore_global
    ```

4.  **Install Zsh plugins and tools**
    * Follow the instructions for Powerlevel10k to install and configure it.
    * Run `brew install zsh-autosuggestions zsh-syntax-highlighting`
    * Install `thefuck` and other tools as needed.

5.  **Install Neovim plugins**
    * Open Neovim and run `:Lazy`. This will install all the plugins.
    * Run `:MasonInstallAll` to install all the LSP servers, linters, formatters, and debuggers.

6.  **Setup VSCode (Optional)**
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
* **Buffer & Tab Management**
    * `<leader>to`: Open new tab
    * `<leader>tx`: Close current tab
    * `<leader>tn`: Go to next tab
    * `<leader>tp`: Go to previous tab
* **File Explorer**: `<leader>ee` to toggle `nvim-tree`.
* **Fuzzy Finding**:
    * `<leader>ff`: Find files
    * `<leader>fs`: Live grep string
* **Git**: `[h` and `]h` to navigate hunks.

#### Tmux

* **Prefix**: `<C-a>`
* **Splitting Panes**
    * `|`: Split vertically
    * `-`: Split horizontally
* **Resizing Panes**: Use prefix + `h`, `j`, `k`, `l` to resize panes. `m` to maximize/minimize.
* **Vim Integration**: `<C-h>`, `<C-j>`, `<C-k>`, `<C-l>` to navigate between Vim/Neovim splits and tmux panes.
