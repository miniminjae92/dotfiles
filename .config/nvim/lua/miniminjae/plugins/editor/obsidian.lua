-- 볼트를 nvim에서 직접 편집한다. `[[`로 노트를 잇고, 백링크·데일리노트·템플릿을 그대로 쓴다.
-- 볼트 안 파일을 열 때만 붙는다 — 일반 마크다운까지 이 플러그인이 관여하면 무겁다.
local vault = vim.fn.expand("~") .. "/.obsidian"

return {
	"obsidian-nvim/obsidian.nvim",
	version = "*",
	dependencies = { "nvim-lua/plenary.nvim" },
	event = {
		"BufReadPre " .. vault .. "/*/**.md",
		"BufNewFile " .. vault .. "/*/**.md",
	},
	opts = {
		legacy_commands = false,
		workspaces = {
			-- 개발 지식·에이전트 OS 기록
			{
				name = "mimir",
				path = vault .. "/mimir",
				overrides = {
					notes_subdir = "00 Inbox",
					templates = { folder = "_System/Templates" },
				},
			},
			-- 개인 노트·일기·글감
			{
				name = "yggdrasil",
				path = vault .. "/yggdrasil",
				overrides = {
					notes_subdir = "0-inbox",
					templates = { folder = "_templates" },
					daily_notes = {
						folder = "2-me/dairy/1. 일간",
						date_format = "%Y-%m-%d",
					},
				},
			},
		},
		completion = { blink = true, min_chars = 2 },
		-- 렌더링은 render-markdown.nvim이 이미 하고 있다. 둘 다 켜면 화면이 겹친다.
		ui = { enable = false },
	},
	keys = {
		{ "<leader>on", "<cmd>Obsidian new<cr>", desc = "새 노트" },
		{ "<leader>oo", "<cmd>Obsidian quick_switch<cr>", desc = "노트 바로 열기" },
		{ "<leader>os", "<cmd>Obsidian search<cr>", desc = "볼트 전문 검색" },
		{ "<leader>od", "<cmd>Obsidian today<cr>", desc = "오늘 일간 노트" },
		{ "<leader>ot", "<cmd>Obsidian template<cr>", desc = "템플릿 삽입" },
		{ "<leader>ob", "<cmd>Obsidian backlinks<cr>", desc = "이 노트를 가리키는 곳" },
		{ "<leader>ol", "<cmd>Obsidian links<cr>", desc = "이 노트가 가리키는 곳" },
		{ "<leader>ow", "<cmd>Obsidian workspace<cr>", desc = "볼트 전환" },
	},
}
