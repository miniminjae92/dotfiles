-- 색 테마. 터미널 배경을 그대로 비치게 두려고 transparent를 켠다.
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
		vim.cmd([[colorscheme solarized-osaka]])
	end,
}
