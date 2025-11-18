-- plugins/lsp/mason.lua
return {
	"williamboman/mason.nvim",
	dependencies = {
		"williamboman/mason-lspconfig.nvim",
		"WhoIsSethDaniel/mason-tool-installer.nvim",
	},
	config = function()
		-- import mason
		local mason = require("mason")

		-- import mason-lspconfig
		local mason_lspconfig = require("mason-lspconfig")

		local mason_tool_installer = require("mason-tool-installer")

		-- enable mason and configure icons
		mason.setup({
			ui = {
				icons = {
					package_installed = "✓",
					package_pending = "➜",
					package_uninstalled = "✗",
				},
			},
		})

		mason_lspconfig.setup({
			-- LSP 서버 자동 설치 목록
			ensure_installed = {
				"html",
				"cssls",
				"tailwindcss",
				"svelte",
				"lua_ls",
				"graphql",
				"emmet_ls",
				"pyright",
				"ts_ls",
				"jdtls",
				"clangd", -- C/C++ LSP server
			},
		})

		mason_tool_installer.setup({
			ensure_installed = {
				-- 포매터
				"prettierd",
				"stylua",
				"google-java-format",

				-- 린터 & 포매터 통합 (Python)
				"ruff",

				-- FE 린터
				"eslint_d",

				-- 디버거
				"java-debug-adapter",
				"java-test",
			},
		})
	end,
}
