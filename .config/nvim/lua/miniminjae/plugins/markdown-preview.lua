-- plugins/markdown-preview.lua
return {
	-- install with yarn or npm
	{
		"iamcco/markdown-preview.nvim",
		cmd = { "MarkdownPreviewToggle", "MarkdownPreview", "MarkdownPreviewStop" },
		build = "cd app && yarn install",
		init = function()
			vim.g.mkdp_filetypes = { "markdown" }
			vim.g.mkdp_markdown_css = vim.fn.stdpath("config") .. "/assets/markdown-reader.css"
			vim.g.mkdp_theme = vim.o.background == "light" and "light" or "dark"
		end,
		ft = { "markdown" },
		config = function()
			vim.keymap.set("n", "<leader>mp", "<cmd>MarkdownPreview<CR>", { desc = "Markdown Preview" })
			vim.keymap.set("n", "<leader>ms", "<cmd>MarkdownPreviewStop<CR>", { desc = "Stop Markdown Preview" })
			vim.keymap.set("n", "<leader>mt", "<cmd>MarkdownPreviewToggle<CR>", { desc = "Toggle Markdown Preview" })
			vim.keymap.set("n", "<leader>ml", function()
				vim.g.mkdp_theme = vim.g.mkdp_theme == "light" and "dark" or "light"
				vim.cmd("MarkdownPreviewStop")
				vim.defer_fn(function()
					vim.cmd("MarkdownPreview")
				end, 100)
				vim.notify("Markdown Preview theme: " .. vim.g.mkdp_theme)
			end, { desc = "Toggle Markdown Preview Light/Dark" })
		end,
	},
}
