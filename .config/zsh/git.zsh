# git 약어 — oh-my-zsh git 플러그인 이름 규약을 따르되 omz 의존은 없다.
#
# 왜 전량(197개)이 아니라 큐레이션인가:
#   omz를 쓰던 시절 히스토리에 실제로 등장한 약어는 197개 중 22개뿐이었다.
#   나머지 175개는 한 번도 쓰이지 않았다. 이 파일은 그 22개 + 바로 옆 변형만 담는다.
#
# 이름은 upstream omz(plugins/git/git.plugin.zsh)와 글자 단위로 일치시킨다.
# 손가락 기억이 그대로 먹고, 나중에 하나 더 필요하면 그 파일에서 한 줄 복사하면 된다.
# 조회용 원본: https://github.com/ohmyzsh/ohmyzsh/blob/master/plugins/git/git.plugin.zsh
#
# 추가할 때 규칙: upstream에 있는 이름이면 정의도 그대로 베낀다. 임의로 짓지 않는다.

# ---- 헬퍼 (omz lib/git.zsh 대체, 자립 구현) ----

# 현재 브랜치명. detached HEAD면 짧은 해시. git repo가 아니면 조용히 빈 값.
git_current_branch() {
  local ref
  ref=$(command git symbolic-ref --quiet HEAD 2>/dev/null) && { echo "${ref#refs/heads/}"; return 0; }
  [[ $? == 128 ]] && return           # git repo 아님
  command git rev-parse --short HEAD 2>/dev/null
}

# 기본 브랜치명. main/master 등을 순서대로 탐색한다 (omz git_main_branch 축약본).
git_main_branch() {
  command git rev-parse --git-dir &>/dev/null || return
  local ref
  for ref in refs/{heads,remotes/{origin,upstream}}/{main,trunk,mainline,default,stable,master}; do
    command git show-ref -q --verify "$ref" && { echo "${ref##*/}"; return 0; }
  done
  echo master
}

# ---- 기본 ----

alias g='git'
alias gst='git status'
alias gss='git status --short'
alias gsb='git status --short --branch'

# ---- add / commit ----

alias ga='git add'
alias gaa='git add --all'
alias gap='git apply'
alias gc='git commit --verbose'
alias gca='git commit --verbose --all'
alias gcmsg='git commit --message'
alias gcam='git commit --all --message'
alias gcn='git commit --verbose --no-edit'

# ---- branch ----

alias gb='git branch'
alias gba='git branch --all'
alias gbr='git branch --remote'
alias gbd='git branch --delete'
alias gbD='git branch --delete --force'

# ---- checkout / switch ----

alias gco='git checkout'
alias gcb='git checkout -b'
alias gcm='git checkout $(git_main_branch)'
alias gsw='git switch'
alias gswc='git switch --create'
alias gswm='git switch $(git_main_branch)'

# ---- diff ----

alias gd='git diff'
alias gds='git diff --staged'
alias gdca='git diff --cached'
alias gdw='git diff --word-diff'

# ---- log ----

alias glog='git log --oneline --decorate --graph'
alias glo='git log --oneline --decorate'
alias glg='git log --stat'
alias glol='git log --graph --pretty="%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%ar) %C(bold blue)<%an>%Creset"'
alias gwch='git log --patch --abbrev-commit --pretty=medium --raw'

# ---- fetch / pull / push ----

alias gf='git fetch'
alias gfo='git fetch origin'
alias gl='git pull'
alias gp='git push'
alias gpsup='git push --set-upstream origin $(git_current_branch)'
alias ggpush='git push origin "$(git_current_branch)"'
alias ggpull='git pull origin "$(git_current_branch)"'

# --force-with-lease. --force는 일부러 넣지 않는다.
ggfl() {
  local b
  [[ $# != 1 ]] && b="$(git_current_branch)"
  git push --force-with-lease origin "${b:-$1}"
}

# ---- stash ----

alias gsta='git stash push'
alias gstu='git stash push --include-untracked'
alias gstp='git stash pop'
alias gstl='git stash list'
alias gsts='git stash show --patch'
alias gstd='git stash drop'

# ---- rebase / merge ----

alias grb='git rebase'
alias grbi='git rebase --interactive'
alias grbc='git rebase --continue'
alias grba='git rebase --abort'
alias grbm='git rebase $(git_main_branch)'
alias gm='git merge'
alias gmom='git merge origin/$(git_main_branch)'

# ---- reset / restore ----

alias grh='git reset'
alias grhh='git reset --hard'
alias grs='git restore'
alias grst='git restore --staged'

# ---- cherry-pick / revert ----

alias gcp='git cherry-pick'
alias gcpc='git cherry-pick --continue'
alias gcpa='git cherry-pick --abort'
alias grev='git revert'

# ---- worktree ----

alias gwt='git worktree'

# ---- WIP 관용구 ----

alias gwip='git add -A; git rm $(git ls-files --deleted) 2> /dev/null; git commit --no-verify --no-gpg-sign --message "--wip-- [skip ci]"'
alias gunwip='git rev-list --max-count=1 --format="%s" HEAD | grep -q "\--wip--" && git reset HEAD~1'
