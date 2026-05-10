#!/usr/bin/env bash
set -euo pipefail

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/.dotfiles}"

link_file() {
  local source="$1"
  local target="$2"

  mkdir -p "$(dirname "$target")"

  if [ -e "$target" ] && [ ! -L "$target" ]; then
    printf 'skip: %s already exists and is not a symlink\n' "$target" >&2
    return
  fi

  ln -sfn "$source" "$target"
}

link_file "$DOTFILES_DIR/.gitconfig" "$HOME/.gitconfig"
link_file "$DOTFILES_DIR/.gitignore" "$HOME/.gitignore"
link_file "$DOTFILES_DIR/.vimrc" "$HOME/.vimrc"
link_file "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
link_file "$DOTFILES_DIR/.tmux.conf" "$HOME/.tmux.conf"
link_file "$DOTFILES_DIR/.config/nvim" "$HOME/.config/nvim"
link_file "$DOTFILES_DIR/.gitignore" "$HOME/.gitignore_global"
link_file \
  "$DOTFILES_DIR/.config/commit-message-conventions/angular.md" \
  "$HOME/.config/commit-message-conventions/angular.md"
link_file \
  "$DOTFILES_DIR/.config/lazygit/config.yml" \
  "$HOME/Library/Application Support/lazygit/config.yml"

git config --global core.excludesFile "$HOME/.gitignore_global"

printf 'Installed dotfile links.\n'
printf 'Open a new shell or run: exec zsh\n'
