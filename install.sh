#!/usr/bin/env bash
set -euo pipefail

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/.dotfiles}"
REPLACE_EXISTING=0
SKIPPED_LINKS=()

if [ "${1:-}" = "--replace" ]; then
  REPLACE_EXISTING=1
fi

link_file() {
  local source="$1"
  local target="$2"

  if [ ! -e "$source" ]; then
    printf 'missing source: %s\n' "$source" >&2
    return
  fi

  mkdir -p "$(dirname "$target")"

  if [ -e "$target" ] && [ ! -L "$target" ]; then
    if [ "$REPLACE_EXISTING" -eq 1 ]; then
      local backup="${target}.bak.$(date +%Y%m%d%H%M%S)"
      mv "$target" "$backup"
      printf 'backup: %s -> %s\n' "$target" "$backup"
    else
      printf 'skip: %s already exists and is not a symlink\n' "$target" >&2
      SKIPPED_LINKS+=("$target")
      return
    fi
  fi

  ln -sfn "$source" "$target"
}

link_file "$DOTFILES_DIR/.gitconfig" "$HOME/.gitconfig"
link_file "$DOTFILES_DIR/.gitignore" "$HOME/.gitignore"
link_file "$DOTFILES_DIR/.vimrc" "$HOME/.vimrc"
link_file "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
link_file "$DOTFILES_DIR/.tmux.conf" "$HOME/.tmux.conf"
link_file "$DOTFILES_DIR/.ideavimrc" "$HOME/.ideavimrc"
link_file "$DOTFILES_DIR/.config/nvim" "$HOME/.config/nvim"
link_file \
  "$DOTFILES_DIR/.config/bat/themes/tokyonight_night.tmTheme" \
  "$HOME/.config/bat/themes/tokyonight_night.tmTheme"
link_file "$DOTFILES_DIR/.codex/AGENTS.md" "$HOME/.codex/AGENTS.md"
if [ -d "$DOTFILES_DIR/.codex/skills" ]; then
  for skill_dir in "$DOTFILES_DIR"/.codex/skills/*; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    link_file "$skill_dir" "$HOME/.codex/skills/$skill_name"
  done
fi
link_file "$DOTFILES_DIR/.gitignore" "$HOME/.gitignore_global"
if [ -d "$DOTFILES_DIR/bin" ]; then
  for script_path in "$DOTFILES_DIR"/bin/*; do
    [ -f "$script_path" ] || continue
    script_name="$(basename "$script_path")"
    link_file "$script_path" "$HOME/.local/bin/$script_name"
  done
fi
link_file \
  "$DOTFILES_DIR/conventions/commit-message/angular.md" \
  "$HOME/.config/commit-message-conventions/angular.md"
link_file \
  "$DOTFILES_DIR/conventions/commit-message/korean-angularjs.md" \
  "$HOME/.config/commit-message-conventions/korean-angularjs.md"
link_file \
  "$DOTFILES_DIR/.config/lazygit/config.yml" \
  "$HOME/Library/Application Support/lazygit/config.yml"

git config --global core.excludesFile "$HOME/.gitignore_global"

if command -v bat >/dev/null 2>&1; then
  bat cache --build
fi

printf 'Installed dotfile links.\n'
printf 'Open a new shell or run: exec zsh\n'

if [ "${#SKIPPED_LINKS[@]}" -gt 0 ]; then
  printf 'Skipped regular files that were not replaced:\n' >&2
  printf '  %s\n' "${SKIPPED_LINKS[@]}" >&2
  printf 'Run with --replace to back them up and restore symlinks.\n' >&2
fi
