# Powerlevel10k instant prompt (iTerm2 & others; Ghostty uses Starship below).
# Console-input init must go above this block; everything else may go below.
if [[ "$TERM_PROGRAM" != "ghostty" && -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export LANG="en_US.UTF-8"
export EDITOR="vim"

# Keep PATH entries unique — dedups even if installers re-append later.
typeset -U path PATH

# Homebrew prefix (cached once; portable across Apple Silicon / Intel).
export HOMEBREW_PREFIX="${HOMEBREW_PREFIX:-$(brew --prefix)}"

# Completion system (previously initialized by oh-my-zsh).
fpath=("$HOMEBREW_PREFIX/share/zsh/site-functions" $fpath)
autoload -Uz compinit && compinit

# Completion matching, restored from oh-my-zsh's lib/completion.zsh (dropped with omz).
# 'l:|=* r:|=*' is the substring rule: `cd api<TAB>` → delivery-discount-api/.
zstyle ':completion:*' matcher-list 'm:{[:lower:][:upper:]}={[:upper:][:lower:]}' 'r:|=*' 'l:|=* r:|=*'
zstyle ':completion:*' menu select

# Autosuggestions (syntax-highlighting is sourced last, at end of file).
source "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh"

# Prompt: Ghostty gets Starship (A/B trial); iTerm2 & others keep Powerlevel10k.
if [[ "$TERM_PROGRAM" == "ghostty" ]]; then
  eval "$(starship init zsh)"
else
  source "$HOMEBREW_PREFIX/share/powerlevel10k/powerlevel10k.zsh-theme"
  # To customize the p10k prompt, run `p10k configure` or edit ~/.p10k.zsh.
  [[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
fi

# Shell behavior
unsetopt beep

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
# uv manages Python versions/venvs now (pyenv retired 2026-08-04)
export PKG_CONFIG_PATH="$(brew --prefix tcl-tk@8)/lib/pkgconfig"

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


# ---- git alias ----
# 본체는 .config/zsh/git.zsh (install.sh가 ~/.config/zsh/ 로 링크한다).
# oh-my-zsh git 플러그인 이름 규약을 따르되 omz 의존은 없다.

[ -r "$HOME/.config/zsh/git.zsh" ] && source "$HOME/.config/zsh/git.zsh"

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

# ---- Zoxide (better cd) ----
# init은 PATH 조작이 모두 끝난 뒤 실행해야 doctor 경고가 없다 (syntax highlighting 직전).
# 에이전트 툴 셸(Claude Code)은 chpwd 훅이 유실돼 doctor가 오탐하므로 검사만 끈다.
[ -n "${CLAUDECODE:-}" ] && export _ZO_DOCTOR=0
eval "$(zoxide init zsh)"
alias cd="z"

# Syntax highlighting must be sourced last (after all zle widgets are defined).
source "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
