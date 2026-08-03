-- 마크다운을 "읽기 좋게" 만드는 네 가지: 버퍼 안 렌더 / 브라우저 미리보기 / 이미지 붙여넣기 / 표 정렬.
return {
	-- 편집 중인 버퍼에서 헤딩·코드블록·표를 바로 렌더한다
	{
		"MeanderingProgrammer/render-markdown.nvim",
		ft = { "markdown", "mdx" },
		opts = {
			file_types = { "markdown", "mdx" },
			code = { sign = false, width = "block", right_pad = 1 },
			heading = { sign = false, icons = {} },
		},
	},

	-- 브라우저 미리보기. mermaid 다이어그램도 여기서 네이티브로 렌더된다.
	{
		"iamcco/markdown-preview.nvim",
		cmd = { "MarkdownPreviewToggle", "MarkdownPreview", "MarkdownPreviewStop" },
		ft = { "markdown" },
		build = "cd app && yarn install",
		init = function()
			vim.g.mkdp_filetypes = { "markdown" }
			vim.g.mkdp_markdown_css = vim.fn.stdpath("config") .. "/assets/markdown-reader.css"
			vim.g.mkdp_theme = vim.o.background == "light" and "light" or "dark"
		end,
		keys = {
			{ "<leader>mp", "<cmd>MarkdownPreview<CR>", desc = "미리보기 시작" },
			{ "<leader>ms", "<cmd>MarkdownPreviewStop<CR>", desc = "미리보기 중지" },
			{ "<leader>mt", "<cmd>MarkdownPreviewToggle<CR>", desc = "미리보기 토글" },
			{
				"<leader>ml",
				function()
					vim.g.mkdp_theme = vim.g.mkdp_theme == "light" and "dark" or "light"
					vim.cmd("MarkdownPreviewStop")
					vim.defer_fn(function()
						vim.cmd("MarkdownPreview")
					end, 100)
					vim.notify("미리보기 테마: " .. vim.g.mkdp_theme)
				end,
				desc = "미리보기 밝기 전환",
			},
		},
	},

	-- 클립보드 이미지를 파일로 저장하고 링크까지 써 넣는다
	{
		"HakonHarnes/img-clip.nvim",
		event = "VeryLazy",
		opts = {
			default = {
				dir_path = ".",
				file_name = "%Y-%m-%d-%H-%M-%S",
				use_absolute_path = false,
				relative_to_current_file = true,
			},
		},
		keys = {
			{ "<leader>p", "<cmd>PasteImage<cr>", desc = "클립보드 이미지 붙여넣기" },
		},
	},

	-- 표 칸 맞추기 (gqip로 문단 전체 정렬)
	{
		"dhruvasagar/vim-table-mode",
		cmd = "TableModeToggle",
		init = function()
			vim.g.table_mode_corner = "|"
			vim.g.table_mode_separator = "|"
			vim.g.table_mode_fillchar = "-"
			vim.g.table_mode_auto_choose_table_mode = 1
			vim.g.table_mode_default_style = "markdown"
			vim.g.table_mode_auto_align = 1
		end,
		keys = {
			{ "<leader>tm", "<cmd>TableModeToggle<CR>", desc = "표 모드 토글" },
		},
	},
}
