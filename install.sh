#!/usr/bin/env bash
set -euo pipefail

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/.dotfiles}"
REPLACE_EXISTING=0
SKIPPED_LINKS=()
LAUNCHD_FAILURES=()

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

# launchd 잡 하나를 내렸다가 다시 올린다.
#
# `launchctl bootout` 은 반환해도 해체가 끝난 게 아니다. 곧바로 bootstrap 하면
# EIO(5, "Input/output error") 로 실패한다. 그래서 해체 완료를 확인한 뒤 올리고,
# 그래도 실패하면 몇 번 더 시도한다.
#
# 실패해도 스크립트를 죽이지 않는다. set -e 아래에서 bootstrap 하나가 죽으면
# 이후 심볼릭 링크·설정 병합·bat 캐시까지 통째로 건너뛰는 사고가 실제로 있었다.
# 잡 재적재는 설치의 마지막 단계이지 전제 조건이 아니다.
reload_agent() {
  local label="$1"
  local plist="$2"
  local domain="gui/$(id -u)"
  local attempt

  launchctl bootout "$domain/$label" >/dev/null 2>&1 || true

  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    launchctl print "$domain/$label" >/dev/null 2>&1 || break
    sleep 0.2
  done

  for attempt in 1 2 3; do
    if launchctl bootstrap "$domain" "$plist" 2>/dev/null; then
      return 0
    fi
    sleep 0.5
  done

  printf 'warn: launchctl bootstrap failed: %s\n' "$label" >&2
  LAUNCHD_FAILURES+=("$label")
}

build_agent_notify_menu() {
  # 소스는 추출 레포(D-022 개정, Wave 3)에 있다 — 클론 없으면 건너뛴다.
  local source="$HOME/projects/agent-notify/agent-notify-menu/AgentNotifyMenu.swift"
  local plist="$HOME/projects/agent-notify/agent-notify-menu/Info.plist"
  local app="$HOME/Applications/AgentNotifyMenu.app"
  local contents="$app/Contents"
  local executable="$contents/MacOS/AgentNotifyMenu"
  local temporary_executable="${executable}.tmp.$$"
  local module_cache="${TMPDIR:-/private/tmp}/agent-notify-menu-module-cache"

  if [ ! -f "$source" ]; then
    printf 'skip: AgentNotifyMenu (클론 없음: %s)\n' "$source"
    return
  fi
  if ! command -v xcrun >/dev/null 2>&1; then
    printf 'skip: xcrun unavailable; AgentNotifyMenu was not built\n' >&2
    return
  fi

  mkdir -p "$contents/MacOS" "$module_cache"
  cp "$plist" "$contents/Info.plist"
  CLANG_MODULE_CACHE_PATH="$module_cache" \
    SWIFT_MODULECACHE_PATH="$module_cache" \
    xcrun swiftc "$source" -o "$temporary_executable" -framework AppKit
  mv "$temporary_executable" "$executable"
  chmod 755 "$executable"
  if command -v codesign >/dev/null 2>&1; then
    codesign --force --sign - "$app" >/dev/null
  fi
}

link_file "$DOTFILES_DIR/.gitconfig" "$HOME/.gitconfig"
link_file "$DOTFILES_DIR/.gitignore" "$HOME/.gitignore"
link_file "$DOTFILES_DIR/.vimrc" "$HOME/.vimrc"
link_file "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
link_file "$DOTFILES_DIR/.tmux.conf" "$HOME/.tmux.conf"
link_file "$DOTFILES_DIR/.ideavimrc" "$HOME/.ideavimrc"
link_file "$DOTFILES_DIR/.config/nvim" "$HOME/.config/nvim"
link_file "$DOTFILES_DIR/.config/zsh/git.zsh" "$HOME/.config/zsh/git.zsh"
link_file "$DOTFILES_DIR/.config/starship.toml" "$HOME/.config/starship.toml"
link_file "$DOTFILES_DIR/.config/ghostty/config" "$HOME/.config/ghostty/config"
link_file \
  "$DOTFILES_DIR/.config/bat/themes/tokyonight_night.tmTheme" \
  "$HOME/.config/bat/themes/tokyonight_night.tmTheme"
link_file \
  "$DOTFILES_DIR/.config/agent-notify/config.json" \
  "$HOME/.config/agent-notify/config.json"
link_file "$DOTFILES_DIR/agents/AGENTS.md" "$HOME/.codex/AGENTS.md"
link_file "$DOTFILES_DIR/agents/AGENTS.md" "$HOME/.gemini/GEMINI.md"
link_file "$DOTFILES_DIR/agents/claude/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
link_file "$DOTFILES_DIR/agents/codex/hooks.json" "$HOME/.codex/hooks.json"
link_file "$DOTFILES_DIR/agents/gemini/hooks.json" "$HOME/.gemini/config/hooks.json"
if [ -d "$DOTFILES_DIR/agents/codex/agents" ]; then
  for agent_path in "$DOTFILES_DIR"/agents/codex/agents/*.toml; do
    [ -f "$agent_path" ] || continue
    agent_name="$(basename "$agent_path")"
    link_file "$agent_path" "$HOME/.codex/agents/$agent_name"
  done
fi
if [ -d "$DOTFILES_DIR/agents/codex/skills" ]; then
  for skill_dir in "$DOTFILES_DIR"/agents/codex/skills/*; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    link_file "$skill_dir" "$HOME/.codex/skills/$skill_name"
  done
fi
if [ -d "$DOTFILES_DIR/agents/claude/skills" ]; then
  for skill_dir in "$DOTFILES_DIR"/agents/claude/skills/*; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    link_file "$skill_dir" "$HOME/.claude/skills/$skill_name"
  done
fi
if [ -d "$DOTFILES_DIR/agents/skills" ]; then
  for skill_dir in "$DOTFILES_DIR"/agents/skills/*; do
    [ -d "$skill_dir" ] || continue
    skill_name="$(basename "$skill_dir")"
    link_file "$skill_dir" "$HOME/.codex/skills/$skill_name"
    link_file "$skill_dir" "$HOME/.claude/skills/$skill_name"
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
# 독립 저장소로 이관된 도구(D-022) — 클론이 있으면 링크, 없으면 건너뛴다
# (예: 아이맥처럼 필요할 때만 clone하는 기기).
for external_tool in \
  "agent-notify:$HOME/projects/agent-notify/bin/agent-notify" \
  "mdview:$HOME/projects/mdview/mdview" \
  "kman:$HOME/projects/kman/bin/kman" \
  "video-summary:$HOME/projects/video-summary/bin/video-summary" \
  "git-ai-commit:$HOME/projects/git-ai-commit/bin/git-ai-commit" \
  "git-plan-ai:$HOME/projects/git-ai-commit/bin/git-plan-ai" \
  "lazygit-ai-commit:$HOME/projects/git-ai-commit/bin/lazygit-ai-commit"
do
  tool_name="${external_tool%%:*}"
  tool_path="${external_tool#*:}"
  if [ -f "$tool_path" ]; then
    link_file "$tool_path" "$HOME/.local/bin/$tool_name"
  else
    echo "skip: $tool_name (클론 없음: $tool_path)"
  fi
done
# 모델 레지스트리 — 추출 도구(git-ai-commit·video-summary)의 XDG 기본 경로
link_file \
  "$DOTFILES_DIR/agents/models.json" \
  "$HOME/.config/ai-tools/models.json"
link_file \
  "$DOTFILES_DIR/agents/conventions/commit-message/angular.md" \
  "$HOME/.config/commit-message-conventions/angular.md"
link_file \
  "$DOTFILES_DIR/agents/conventions/commit-message/korean-angularjs.md" \
  "$HOME/.config/commit-message-conventions/korean-angularjs.md"
link_file \
  "$DOTFILES_DIR/agents/models.json" \
  "$HOME/.config/ai-tools/models.json"
link_file \
  "$DOTFILES_DIR/.config/lazygit/config.yml" \
  "$HOME/Library/Application Support/lazygit/config.yml"

if [ "$(uname -s)" = "Darwin" ]; then
  build_agent_notify_menu
  menu_plist="$HOME/Library/LaunchAgents/com.miniminjae.agent-notify-menu.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.agent-notify-menu.plist" \
    "$menu_plist"
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
  harvest_daily_plist="$HOME/Library/LaunchAgents/com.miniminjae.session-harvest-daily.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.session-harvest-daily.plist" \
    "$harvest_daily_plist"
  harvest_weekly_plist="$HOME/Library/LaunchAgents/com.miniminjae.session-harvest-weekly.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.session-harvest-weekly.plist" \
    "$harvest_weekly_plist"
  ops_digest_plist="$HOME/Library/LaunchAgents/com.miniminjae.ops-digest-daily.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.ops-digest-daily.plist" \
    "$ops_digest_plist"
  simulator_reaper_plist="$HOME/Library/LaunchAgents/com.miniminjae.simulator-reaper.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.simulator-reaper.plist" \
    "$simulator_reaper_plist"
  # 원천 미러링(맥북 → 아이맥). 두 기기 공용이라 아이맥에도 설치되지만,
  # 스크립트가 원격=자기자신을 감지해 no-op 으로 끝낸다.
  mirror_imac_plist="$HOME/Library/LaunchAgents/com.miniminjae.mirror-to-imac.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.mirror-to-imac.plist" \
    "$mirror_imac_plist"
  mirror_from_imac_plist="$HOME/Library/LaunchAgents/com.miniminjae.mirror-from-imac.plist"
  link_file \
    "$DOTFILES_DIR/.config/launchd/com.miniminjae.mirror-from-imac.plist" \
    "$mirror_from_imac_plist"
  mkdir -p \
    "$HOME/.local/state/agent-notify" \
    "$HOME/.local/state/agent-os" \
    "$HOME/.local/state/codex-account-usage" \
    "$HOME/.local/state/mirror-to-imac" \
    "$HOME/.local/state/ops" \
    "$HOME/.local/state/personal-ops" \
    "$HOME/.local/state/session-harvest" \
    "$HOME/.local/state/simulator-reaper"
  reload_agent com.miniminjae.agent-notify-sweep "$notification_plist"
  reload_agent com.miniminjae.agent-notify-menu "$menu_plist"
  reload_agent com.miniminjae.agent-os-vault-snapshot "$snapshot_plist"
  reload_agent com.miniminjae.codex-account-usage "$usage_plist"
  reload_agent com.miniminjae.personal-ops-security "$security_plist"
  # 은퇴: personal-ops-weekly → session-harvest-weekly로 대체(2026-07-22). bootout만, 재부트스트랩 안 함.
  launchctl bootout "gui/$(id -u)/com.miniminjae.personal-ops-weekly" >/dev/null 2>&1 || true
  rm -f "$HOME/Library/LaunchAgents/com.miniminjae.personal-ops-weekly.plist"
  reload_agent com.miniminjae.session-harvest-daily "$harvest_daily_plist"
  reload_agent com.miniminjae.session-harvest-weekly "$harvest_weekly_plist"
  reload_agent com.miniminjae.ops-digest-daily "$ops_digest_plist"
  reload_agent com.miniminjae.simulator-reaper "$simulator_reaper_plist"
  reload_agent com.miniminjae.mirror-to-imac "$mirror_imac_plist"
  reload_agent com.miniminjae.mirror-from-imac "$mirror_from_imac_plist"
fi

# Merge managed Claude Code settings into the machine-local settings file.
# settings.json stays unlinked because Claude Code rewrites it at runtime
# (model preference, theme); only missing keys and hook events are added,
# and existing entries are never overwritten.
python3 - "$DOTFILES_DIR/agents/claude/settings-fragment.json" "$HOME/.claude/settings.json" <<'PY'
import json, pathlib, sys

fragment_path, settings_path = map(pathlib.Path, sys.argv[1:3])
fragment = json.loads(fragment_path.read_text())
settings_path.parent.mkdir(parents=True, exist_ok=True)
settings = json.loads(settings_path.read_text()) if settings_path.exists() else {}

added = []
hooks = settings.setdefault("hooks", {})
for event in fragment.get("hooks", {}):
    if event not in hooks:
        hooks[event] = fragment["hooks"][event]
        added.append(f"hooks.{event}")
for key, value in fragment.items():
    if key != "hooks" and key not in settings:
        settings[key] = value
        added.append(key)

if added:
    settings_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n")
    print(f"claude settings added: {', '.join(added)}")
else:
    print("claude settings already configured")
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

if [ "${#LAUNCHD_FAILURES[@]}" -gt 0 ]; then
  printf 'LaunchAgents that failed to load:\n' >&2
  printf '  %s\n' "${LAUNCHD_FAILURES[@]}" >&2
  printf 'Re-run install.sh, or inspect one with: launchctl print gui/$(id -u)/<label>\n' >&2
fi
