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
link_file \
  "$DOTFILES_DIR/.config/agent-notify/config.json" \
  "$HOME/.config/agent-notify/config.json"
link_file "$DOTFILES_DIR/agents/AGENTS.md" "$HOME/.codex/AGENTS.md"
link_file "$DOTFILES_DIR/agents/AGENTS.md" "$HOME/.gemini/GEMINI.md"
link_file "$DOTFILES_DIR/claude/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
link_file "$DOTFILES_DIR/agent-os/hooks.json" "$HOME/.codex/hooks.json"
link_file "$DOTFILES_DIR/agy/hooks.json" "$HOME/.gemini/config/hooks.json"
if [ -d "$DOTFILES_DIR/.codex/agents" ]; then
  for agent_path in "$DOTFILES_DIR"/.codex/agents/*.toml; do
    [ -f "$agent_path" ] || continue
    agent_name="$(basename "$agent_path")"
    link_file "$agent_path" "$HOME/.codex/agents/$agent_name"
  done
fi
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
  "$DOTFILES_DIR/ai-tools/models.json" \
  "$HOME/.config/ai-tools/models.json"
link_file \
  "$DOTFILES_DIR/.config/lazygit/config.yml" \
  "$HOME/Library/Application Support/lazygit/config.yml"

if [ "$(uname -s)" = "Darwin" ]; then
  notification_plist="$HOME/Library/LaunchAgents/com.miniminjae.agent-notify-sweep.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.agent-notify-sweep.plist" \
    "$notification_plist"
  snapshot_plist="$HOME/Library/LaunchAgents/com.miniminjae.agent-os-vault-snapshot.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.agent-os-vault-snapshot.plist" \
    "$snapshot_plist"
  usage_plist="$HOME/Library/LaunchAgents/com.miniminjae.codex-account-usage.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.codex-account-usage.plist" \
    "$usage_plist"
  security_plist="$HOME/Library/LaunchAgents/com.miniminjae.personal-ops-security.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.personal-ops-security.plist" \
    "$security_plist"
  weekly_plist="$HOME/Library/LaunchAgents/com.miniminjae.personal-ops-weekly.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.personal-ops-weekly.plist" \
    "$weekly_plist"
  mkdir -p \
    "$HOME/.local/state/agent-notify" \
    "$HOME/.local/state/agent-os" \
    "$HOME/.local/state/codex-account-usage" \
    "$HOME/.local/state/personal-ops"
  launchctl bootout "gui/$(id -u)/com.miniminjae.agent-notify-sweep" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$(id -u)" "$notification_plist"
  launchctl bootout "gui/$(id -u)/com.miniminjae.agent-os-vault-snapshot" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$(id -u)" "$snapshot_plist"
  launchctl bootout "gui/$(id -u)/com.miniminjae.codex-account-usage" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$(id -u)" "$usage_plist"
  launchctl bootout "gui/$(id -u)/com.miniminjae.personal-ops-security" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$(id -u)" "$security_plist"
  launchctl bootout "gui/$(id -u)/com.miniminjae.personal-ops-weekly" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$(id -u)" "$weekly_plist"
fi

# Merge Claude Code hook config into the machine-local settings file.
# settings.json stays unlinked because Claude Code rewrites it at runtime
# (model preference, theme); only missing hook events are added here.
python3 - "$DOTFILES_DIR/claude/hooks-settings.json" "$HOME/.claude/settings.json" <<'PY'
import json, pathlib, sys

fragment_path, settings_path = map(pathlib.Path, sys.argv[1:3])
fragment = json.loads(fragment_path.read_text())
settings_path.parent.mkdir(parents=True, exist_ok=True)
settings = json.loads(settings_path.read_text()) if settings_path.exists() else {}

hooks = settings.setdefault("hooks", {})
added = [event for event in fragment["hooks"] if event not in hooks]
for event in added:
    hooks[event] = fragment["hooks"][event]

if added:
    settings_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n")
    print(f"claude hooks added: {', '.join(added)}")
else:
    print("claude hooks already configured")
PY

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
