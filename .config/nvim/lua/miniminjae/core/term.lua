-- 터미널 감지. tmux 3.2+가 TERM_PROGRAM을 "tmux"로 덮으므로 GHOSTTY_RESOURCES_DIR를 병행 확인한다.
-- 주의: tmux 서버는 자기를 띄운 터미널의 env를 유지한다(다른 터미널에서 붙으면 판정이 서버 기준으로 남는다).
-- 셸 쪽 쌍둥이: ~/.dotfiles/.zshrc의 _is_ghostty.
local M = {}

function M.in_ghostty()
	return vim.env.TERM_PROGRAM == "ghostty" or vim.env.GHOSTTY_RESOURCES_DIR ~= nil
end

return M
