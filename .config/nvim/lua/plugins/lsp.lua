local keyMapper = require("utils.keyMapper").mapKey

-- -- LSP capabilities
-- local capabilities = vim.lsp.protocol.make_client_capabilities()
-- capabilities = require("cmp_nvim_lsp").default_capabilities(capabilities)

return {
	{
		"williamboman/mason.nvim",
		config = function()
			require("mason").setup()
		end,
	},
	{
		"williamboman/mason-lspconfig.nvim",
		config = function()
			require("mason-lspconfig").setup({
				ensure_installed = { "lua_ls", "clangd" },
			})
		end,
	},
	{
		"neovim/nvim-lspconfig",
		config = function()
			local lspconfig = require("lspconfig")
			lspconfig.lua_ls.setup({
				-- settings = {
				-- 	Lua = {
				-- 		diagnostics = {
				-- 			globals = { "vim" },
				-- 		},
				-- 	},
				-- },
				-- capabilities = capabilities,
			})
			lspconfig.clangd.setup({
				-- capabilities = capabilities,
			})

			keyMapper("K", vim.lsp.buf.hover)
			keyMapper("gd", vim.lsp.buf.definition)
			keyMapper("<leader>ca", vim.lsp.buf.code_action)
		end,
	},
}
