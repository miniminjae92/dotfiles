-- 하단 상태 줄. 모드별 색을 직접 정해 두어 지금 어떤 모드인지 색만 보고 안다.
-- 디자인은 터미널별 독립: Ghostty는 reader-dark 팔레트, 그 외(iTerm2 등)는 기존 네이비 테마.
return {
	"nvim-lualine/lualine.nvim",
	dependencies = { "nvim-tree/nvim-web-devicons" },
	event = "VeryLazy",
	config = function()
		local lazy_status = require("lazy.status")
		local in_ghostty = require("miniminjae.core.term").in_ghostty()

		local colors
		if in_ghostty then
			-- reader-dark(colors/reader-dark.lua와 동일 팔레트)
			colors = {
				blue = "#e29a68", -- normal: 액센트 오렌지
				green = "#a9d68d", -- insert: 문자열 그린
				violet = "#d7a3df", -- visual: 키워드 모브
				yellow = "#e8c77c", -- command: 메타 골드
				red = "#d47f77", -- replace: 파생 테라코타
				fg = "#e7dfd2",
				bg = "#252b2d", -- surface
				inactive_bg = "#343d3f", -- table header
			}
		else
			colors = {
				blue = "#65D1FF",
				green = "#3EFFDC",
				violet = "#FF61EF",
				yellow = "#FFDA7B",
				red = "#FF4A4A",
				fg = "#c3ccdc",
				bg = "#112638",
				inactive_bg = "#2c3043",
			}
		end

		local theme = {
			normal = {
				a = { bg = colors.blue, fg = colors.bg, gui = "bold" },
				b = { bg = colors.bg, fg = colors.fg },
				c = { bg = colors.bg, fg = colors.fg },
			},
			insert = {
				a = { bg = colors.green, fg = colors.bg, gui = "bold" },
				b = { bg = colors.bg, fg = colors.fg },
				c = { bg = colors.bg, fg = colors.fg },
			},
			visual = {
				a = { bg = colors.violet, fg = colors.bg, gui = "bold" },
				b = { bg = colors.bg, fg = colors.fg },
				c = { bg = colors.bg, fg = colors.fg },
			},
			command = {
				a = { bg = colors.yellow, fg = colors.bg, gui = "bold" },
				b = { bg = colors.bg, fg = colors.fg },
				c = { bg = colors.bg, fg = colors.fg },
			},
			replace = {
				a = { bg = colors.red, fg = colors.bg, gui = "bold" },
				b = { bg = colors.bg, fg = colors.fg },
				c = { bg = colors.bg, fg = colors.fg },
			},
			inactive = {
				a = { bg = colors.inactive_bg, fg = colors.fg, gui = "bold" },
				b = { bg = colors.inactive_bg, fg = colors.fg },
				c = { bg = colors.inactive_bg, fg = colors.fg },
			},
		}

		require("lualine").setup({
			options = { theme = theme },
			sections = {
				lualine_x = {
					-- 업데이트가 밀려 있으면 여기 숫자가 뜬다
					{
						lazy_status.updates,
						cond = lazy_status.has_updates,
						color = { fg = in_ghostty and "#e29a68" or "#ff9e64" },
					},
					{ "encoding" },
					{ "fileformat" },
					{ "filetype" },
				},
			},
		})
	end,
}
