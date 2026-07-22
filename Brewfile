# Homebrew bundle for this dotfiles environment.
# Install everything with: brew bundle --file ~/.dotfiles/Brewfile
# Machine-specific extras stay out of this file on purpose.

tap "vjeantet/tap"

# Core shell environment
brew "git"
brew "git-delta"
brew "neovim"
brew "tmux"
brew "eza"
brew "bat"
brew "fzf"
brew "fd"
brew "ripgrep"
brew "zoxide"
brew "jq"
brew "thefuck" # 교체 후보(트랙 2): 업스트림 정체, .zshrc eval 제거와 함께 정리 예정

# Development
brew "gh"
brew "pyenv"
brew "lazygit"

# Agent environment
brew "ollama"          # 로컬 커밋 메시지 모델(qwen2.5-coder), 선택적이지만 models.json이 참조
brew "yt-dlp"          # video-summary 자막 추출
brew "gcalcli"
brew "vjeantet/tap/alerter" # agent-notify 클릭 가능 알림

# GUI
cask "iterm2"
cask "karabiner-elements"
cask "visual-studio-code"
cask "tailscale-app"    # 기기 간 메시 VPN(맥북↔아이맥 원격 SSH/화면공유). up은 계정 로그인 필요
