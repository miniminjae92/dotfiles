-- 색 테마. 터미널 배경을 그대로 비치게 두려고 transparent를 켠다.
-- Ghostty A/B: Ghostty에서는 자작 reader-dark(assets/markdown-reader.css의 다크 팔레트),
-- 그 외(iTerm2 등)에서는 기존 solarized-osaka를 그대로 쓴다.
local term = require("miniminjae.core.term")

return {
	"craftzdog/solarized-osaka.nvim",
	lazy = false,
	priority = 1000,
	config = function()
		require("solarized-osaka").setup({
			style = "dark",
			transparent = true,
			styles = {
				sidebars = "transparent",
				floats = "transparent",
			},
		})

		if term.in_ghostty() then
			local ok, err = pcall(vim.cmd.colorscheme, "reader-dark")
			if ok then
				return
			end
			vim.notify("reader-dark 로드 실패, solarized-osaka로 대체: " .. tostring(err), vim.log.levels.WARN)
		end
		vim.cmd.colorscheme("solarized-osaka")
	end,
}
