-- LSP 도구 공급과 데이터원. 서버를 "어떻게 켤지"는 core/lsp.lua가, "무엇을 설치할지"는 여기가 맡는다.
-- mason-lspconfig는 일부러 쓰지 않는다: 자동 활성화가 jdtls까지 켜버려 이중 기동을 만들었기 때문.
return {
	{
		"mason-org/mason.nvim",
		lazy = false,
		priority = 900,
		dependencies = { "WhoIsSethDaniel/mason-tool-installer.nvim" },
		config = function()
			require("mason").setup({
				ui = {
					border = "rounded",
					icons = { package_installed = "✓", package_pending = "➜", package_uninstalled = "✗" },
				},
			})

			-- 이름은 mason 레지스트리 패키지명이다(서버 이름과 다를 수 있다).
			require("mason-tool-installer").setup({
				ensure_installed = {
					-- LSP 서버
					"lua-language-server",
					"typescript-language-server",
					"html-lsp",
					"css-lsp",
					"tailwindcss-language-server",
					"svelte-language-server",
					"graphql-language-service-cli",
					"emmet-ls",
					"pyright",
					"marksman",
					"mdx-analyzer",
					"clangd",
					"json-lsp",
					"yaml-language-server",
					"jdtls",
					-- 디버그·테스트 번들 (jdtls가 init_options로 물고 들어간다)
					"java-debug-adapter",
					"java-test",
					-- 포매터
					"google-java-format",
					"prettierd",
					"stylua",
					-- 린터 (ruff는 포매터 겸용)
					"ruff",
					"eslint_d",
				},
				run_on_start = true,
				auto_update = false,
			})
		end,
	},

	{
		-- 서버별 기본값(cmd·root_markers·filetypes) 데이터베이스로만 쓴다. setup() 호출은 하지 않는다.
		"neovim/nvim-lspconfig",
		event = { "BufReadPre", "BufNewFile" },
		-- lsp/jsonls.lua·lsp/yamlls.lua가 스키마 목록을 여기서 가져간다
		dependencies = { "b0o/schemastore.nvim" },
		config = function()
			require("miniminjae.core.lsp")
		end,
	},

	{
		-- nvim 설정 lua를 편집할 때만 vim/플러그인 타입을 붙여준다(neodev 후계).
		"folke/lazydev.nvim",
		ft = "lua",
		opts = {
			library = {
				{ path = "${3rd}/luv/library", words = { "vim%.uv" } },
			},
		},
	},
}
