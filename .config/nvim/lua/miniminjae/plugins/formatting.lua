-- plugins/formatting.lua
return {
	"stevearc/conform.nvim",
	event = { "BufReadPre", "BufNewFile" },
	config = function()
		local conform = require("conform")

		conform.setup({
			formatters_by_ft = {
				javascript = { "prettier" },
				typescript = { "prettier" },
				javascriptreact = { "prettier" },
				typescriptreact = { "prettier" },
				svelte = { "prettier" },
				css = { "prettier" },
				html = { "prettier" },
				json = { "prettier" },
				yaml = { "prettier" },
				markdown = { "prettier" },
				graphql = { "prettier" },
				liquid = { "prettier" },
				lua = { "stylua" },
				-- remove isort, black
				python = { "ruff" },
				c = { "forty_two" },
				cpp = { "forty_two" },
				java = { "google-java-format" },
			},
			formatters = {
				forty_two = {
					command = vim.fn.expand("~/.local/bin/c_formatter_42"),
					args = { "$FILENAME" },
					stdin = false,
				},
				black = {
					command = vim.fn.expand("~/.local/share/nvim/mason/bin/black"),
					stdin = false,
				},
			},
			format_on_save = {
				lsp_fallback = true,
				async = false,
				timeout_ms = 1000,
			},
		})

		vim.keymap.set({ "n", "v" }, "<leader>mp", function()
			conform.format({
				lsp_fallback = true,
				async = false,
				timeout_ms = 1000,
			})
		end, { desc = "Format file or range (in visual mode)" })
	end,
}
