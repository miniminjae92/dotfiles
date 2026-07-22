# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export LANG="en_US.UTF-8"
export EDITOR="vim"

# Keep PATH entries unique — dedups even if installers re-append later.
typeset -U path PATH

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="powerlevel10k/powerlevel10k"

plugins=(
  git
  zsh-syntax-highlighting
  zsh-autosuggestions
)

source $ZSH/oh-my-zsh.sh

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# history setup
HISTFILE=$HOME/.zhistory
SAVEHIST=50000
HISTSIZE=50000
setopt share_history 
setopt hist_expire_dups_first
setopt hist_ignore_dups
setopt hist_verify

# Use vi keybindings first, then layer bindings onto the vi insert keymap
# (bindings set before `bindkey -v` are lost when the main keymap switches).
bindkey -v

# History search on arrow keys
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward

# Keep a couple of familiar Emacs bindings available while using vi mode.
bindkey '^A' beginning-of-line
bindkey '^E' end-of-line

# ---- JAVA ----
# Default Java version.
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"

# Switch Java versions with `j <version>` or list installed versions with `j`.
j() {
  if [ -n "$1" ]; then
    export JAVA_HOME=$(/usr/libexec/java_home -v "$1")
    export PATH="$JAVA_HOME/bin:$PATH"
    echo "Switched to Java $1"
    java -version
  else
    /usr/libexec/java_home -V
  fi
}

# ---- Python ----
# export PATH="/opt/homebrew/opt/python@3.13/libexec/bin:$PATH"
# pyenv & pyenv-virtualenv settings
export PKG_CONFIG_PATH="$(brew --prefix tcl-tk@8)/lib/pkgconfig"
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# ---- FZF -----

# Set up fzf key bindings and fuzzy completion
eval "$(fzf --zsh)"

# --- setup fzf theme ---
fg="#CBE0F0"
bg="#011628"
bg_highlight="#143652"
purple="#B388FF"
blue="#06BCE4"
cyan="#2CF9ED"

export FZF_DEFAULT_OPTS="--color=fg:${fg},bg:${bg},hl:${purple},fg+:${fg},bg+:${bg_highlight},hl+:${purple},info:${blue},prompt:${cyan},pointer:${cyan},marker:${cyan},spinner:${cyan},header:${cyan}"

# -- Use fd instead of fzf --

export FZF_DEFAULT_COMMAND="fd --hidden --strip-cwd-prefix --exclude .git"
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND="fd --type=d --hidden --strip-cwd-prefix --exclude .git"

# Use fd (https://github.com/sharkdp/fd) for listing path candidates.
# - The first argument to the function ($1) is the base path to start traversal
# - See the source code (completion.{bash,zsh}) for the details.
_fzf_compgen_path() {
  fd --hidden --exclude .git . "$1"
}

# Use fd to generate the list for directory completion
_fzf_compgen_dir() {
  fd --type=d --hidden --exclude .git . "$1"
}

source ~/fzf-git.sh/fzf-git.sh

show_file_or_dir_preview="if [ -d {} ]; then eza --tree --color=always {} | head -200; else bat -n --color=always --line-range :500 {}; fi"

export FZF_CTRL_T_OPTS="--preview '$show_file_or_dir_preview'"
export FZF_ALT_C_OPTS="--preview 'eza --tree --color=always {} | head -200'"

# Advanced customization of fzf options via _fzf_comprun function
# - The first argument to the function is the name of the command.
# - You should make sure to pass the rest of the arguments to fzf.
_fzf_comprun() {
  local command=$1
  shift

  case "$command" in
    cd)           fzf --preview 'eza --tree --color=always {} | head -200' "$@" ;;
    export|unset) fzf --preview "eval 'echo \${}'"         "$@" ;;
    ssh)          fzf --preview 'dig {}'                   "$@" ;;
    *)            fzf --preview "$show_file_or_dir_preview" "$@" ;;
  esac
}

# ----- Bat (better cat) -----

export BAT_THEME=tokyonight_night

# ---- Eza (better ls) -----

alias ls="eza --icons=always"
alias l="ls -la"

# ---- Zoxide (better cd) ----
eval "$(zoxide init zsh)"

alias cd="z"

# ---- git alias ----

alias gst="git status"
alias gaa="git add ."
alias gcmsg="git commit -m"
alias gp="git push"

# Created by `pipx` on 2025-05-04 06:36:44
export PATH="$HOME/.local/bin:$PATH"
export MANPATH="$HOME/.dotfiles/man:${MANPATH:-}"

# User alias
alias cl="clear"
alias lg="lazygit"
alias gcalw="gcalcli calw"
alias gcala="gcalcli agenda"
alias pc="pbcopy"
alias vsummary="video-summary"

# ---- Codex workflows ----
work() {
  local root
  root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  local work_dir="$root/.codex/work"
  local template_dir="$HOME/.dotfiles/.codex/templates/work"
  local editor_cmd="${EDITOR:-nvim}"
  mkdir -p "$work_dir"

  if [ ! -f "$work_dir/TASK.md" ]; then
    cp "$template_dir/TASK.md" "$work_dir/TASK.md"
  fi

  if [ ! -f "$work_dir/DECISIONS.md" ]; then
    cp "$template_dir/DECISIONS.md" "$work_dir/DECISIONS.md"
  fi

  if [ "$#" -eq 0 ]; then
    "$editor_cmd" "$work_dir/TASK.md"
  fi

  codex --cd "$root" "\$work

Use the full work workflow.

Read:
- .codex/work/TASK.md
- .codex/work/DECISIONS.md

Task:
$*"
}

arc() {
  local root
  root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
  local conversation_dir
  if [ -d "$root/docs" ]; then
    conversation_dir="$root/docs/conversation"
  else
    conversation_dir="$root/conversation"
  fi

  local session_ref="${1:-latest}"
  local source_file=""
  local output_slug=""
  local output_dir=""

  mkdir -p "$conversation_dir"

  if [ -f "$session_ref" ]; then
    source_file="$session_ref"
  else
    local date_prefix
    local safe_ref
    date_prefix="$(date +%Y-%m-%d)"
    safe_ref="${session_ref//[^A-Za-z0-9_-]/-}"
    if [ "$safe_ref" = "latest" ]; then
      source_file="$conversation_dir/${date_prefix}-agent-session.md"
    else
      source_file="$conversation_dir/${date_prefix}-agent-session-${safe_ref}.md"
    fi

    local base="${source_file%.md}"
    local counter=2
    while [ -e "$source_file" ]; do
      source_file="${base}-${counter}.md"
      counter=$((counter + 1))
    done

    codex-session-export "$session_ref" "$source_file"
  fi

  output_slug="$(basename "${source_file%.md}")"
  output_dir="$conversation_dir/$output_slug"
  mkdir -p "$output_dir"

  codex --cd "$root" "\$archive-session

Archive this CLI agent conversation into documentation assets.

Source file:
$source_file

Output files:
- $output_dir/raw.md
- $output_dir/keywords.md
- $output_dir/structured.md
- $output_dir/final-notes.md"
}

archive-session() {
  arc "$@"
}

# ---- PR Feedback ----
export PRFB_OUT="$HOME/.obsidian/yggdrasil/3. Resource/GitHub/PR Feedback"

# Gemini CLI Settings
if [ -f "$HOME/.gemini.env" ]; then
	source "$HOME/.gemini.env"
	export GOOGLE_API_KEY
fi

# pnpm
export PNPM_HOME="$HOME/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end

# dotfiles local scripts
export PATH="$HOME/.dotfiles/scripts:$PATH"

# Added by Antigravity
export PATH="$HOME/.antigravity/antigravity/bin:$PATH"
