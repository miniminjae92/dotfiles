-- 저장할 때 코드 모양을 맞춘다. 포맷은 LSP가 아니라 여기가 단독으로 책임진다
-- (jdtls의 format.enabled를 끈 이유도 이것 — 두 곳이 서로 다른 규칙으로 싸우지 않게).
return {
	"stevearc/conform.nvim",
	event = { "BufReadPre", "BufNewFile" },
	opts = {
		formatters_by_ft = {
			javascript = { "prettierd", "prettier", stop_after_first = true },
			typescript = { "prettierd", "prettier", stop_after_first = true },
			javascriptreact = { "prettierd", "prettier", stop_after_first = true },
			typescriptreact = { "prettierd", "prettier", stop_after_first = true },
			svelte = { "prettierd", "prettier", stop_after_first = true },
			css = { "prettierd", "prettier", stop_after_first = true },
			html = { "prettierd", "prettier", stop_after_first = true },
			json = { "prettierd", "prettier", stop_after_first = true },
			yaml = { "prettierd", "prettier", stop_after_first = true },
			markdown = { "prettierd", "prettier", stop_after_first = true },
			graphql = { "prettierd", "prettier", stop_after_first = true },

			lua = { "stylua" },
			python = { "ruff_organize_imports", "ruff_format" },
			java = { "google-java-format" },
		},

		-- java는 google-java-format이 JVM을 새로 띄우느라 1초로는 모자라 저장이 실패한다.
		format_on_save = function(bufnr)
			return {
				lsp_format = "fallback",
				timeout_ms = vim.bo[bufnr].filetype == "java" and 3000 or 1000,
			}
		end,
	},
	keys = {
		{
			"<leader>cf",
			function()
				require("conform").format({ lsp_format = "fallback", timeout_ms = 3000 })
			end,
			mode = { "n", "v" },
			desc = "포맷 (선택 영역 포함)",
		},
	},
}
