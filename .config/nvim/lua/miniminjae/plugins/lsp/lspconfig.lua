-- plugins/lsp/lspconfig.lua
return {
	{
		"neovim/nvim-lspconfig",
		event = { "BufReadPre", "BufNewFile" },
		dependencies = {
			"hrsh7th/cmp-nvim-lsp",
			{ "antosha417/nvim-lsp-file-operations", config = true },
			{ "folke/neodev.nvim", opts = {} },
			"williamboman/mason-lspconfig.nvim",
		},
		config = function()
			-- import lspconfig plugin
			local lspconfig = require("lspconfig")

			-- import mason_lspconfig plugin
			local mason_lspconfig = require("mason-lspconfig")

			-- import cmp-nvim-lsp plugin
			local cmp_nvim_lsp = require("cmp_nvim_lsp")

			local keymap = vim.keymap -- for conciseness

			vim.api.nvim_create_autocmd("LspAttach", {
				group = vim.api.nvim_create_augroup("UserLspConfig", {}),
				callback = function(ev)
					-- Buffer local mappings.
					-- See `:help vim.lsp.*` for documentation on any of the below functions
					local opts = { buffer = ev.buf, silent = true }

					-- set keybinds
					opts.desc = "Show LSP references"
					keymap.set("n", "gR", "<cmd>Telescope lsp_references<CR>", opts) -- show definition, references

					opts.desc = "Go to declaration"
					keymap.set("n", "gD", vim.lsp.buf.declaration, opts) -- go to declaration

					opts.desc = "Show LSP definitions"
					keymap.set("n", "gd", "<cmd>Telescope lsp_definitions<CR>", opts) -- show lsp definitions

					opts.desc = "Show LSP implementations"
					keymap.set("n", "gi", "<cmd>Telescope lsp_implementations<CR>", opts) -- show lsp implementations

					opts.desc = "Show LSP type definitions"
					keymap.set("n", "gt", "<cmd>Telescope lsp_type_definitions<CR>", opts) -- show lsp type definitions

					opts.desc = "See available code actions"
					keymap.set({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, opts) -- see available code actions, in visual mode will apply to selection

					opts.desc = "Smart rename"
					keymap.set("n", "<leader>rn", vim.lsp.buf.rename, opts) -- smart rename

					opts.desc = "Show buffer diagnostics"
					keymap.set("n", "<leader>D", "<cmd>Telescope diagnostics bufnr=0<CR>", opts) -- show  diagnostics for file

					opts.desc = "Show line diagnostics"
					keymap.set("n", "<leader>d", vim.diagnostic.open_float, opts) -- show diagnostics for line

					opts.desc = "Go to previous diagnostic"
					keymap.set("n", "[d", vim.diagnostic.goto_prev, opts) -- jump to previous diagnostic in buffer

					opts.desc = "Go to next diagnostic"
					keymap.set("n", "]d", vim.diagnostic.goto_next, opts) -- jump to next diagnostic in buffer

					opts.desc = "Show documentation for what is under cursor"
					keymap.set("n", "K", vim.lsp.buf.hover, opts) -- show documentation for what is under cursor

					opts.desc = "Restart LSP"
					keymap.set("n", "<leader>rs", ":LspRestart<CR>", opts) -- mapping to restart lsp if necessary
				end,
			})

			-- used to enable autocompletion (assign to every lsp server config)
			local capabilities = cmp_nvim_lsp.default_capabilities()

			vim.diagnostic.config({
				signs = {
					{ name = "DiagnosticSignError", text = "" },
					{ name = "DiagnosticSignWarn", text = "" },
					{ name = "DiagnosticSignHint", text = "󰠠" },
					{ name = "DiagnosticSignInfo", text = "" },
				},
			})

			mason_lspconfig.setup({
				-- default handler for installed servers
				function(server_name)
					lspconfig[server_name].setup({
						capabilities = capabilities,
					})
				end,
				-- configure cpp server
				["clangd"] = function()
					lspconfig["clangd"].setup({
						capabilities = capabilities,
						cmd = { "clangd", "--background-index" },
						filetypes = { "c", "cpp", "objc", "objcpp", "cuda" },
					})
				end,
				["svelte"] = function()
					-- configure svelte server
					lspconfig["svelte"].setup({
						capabilities = capabilities,
						on_attach = function(client, bufnr)
							vim.api.nvim_create_autocmd("BufWritePost", {
								pattern = { "*.js", "*.ts" },
								callback = function(ctx)
									-- Here use ctx.match instead of ctx.file
									client.notify("$/onDidChangeTsOrJsFile", { uri = ctx.match })
								end,
							})
						end,
					})
				end,
				["graphql"] = function()
					-- configure graphql language server
					lspconfig["graphql"].setup({
						capabilities = capabilities,
						filetypes = { "graphql", "gql", "svelte", "typescriptreact", "javascriptreact" },
					})
				end,
				["emmet_ls"] = function()
					-- configure emmet language server
					lspconfig["emmet_ls"].setup({
						capabilities = capabilities,
						filetypes = {
							"html",
							"typescriptreact",
							"javascriptreact",
							"css",
							"sass",
							"scss",
							"less",
							"svelte",
						},
					})
				end,
				["lua_ls"] = function()
					-- configure lua server (with special settings)
					lspconfig["lua_ls"].setup({
						capabilities = capabilities,
						settings = {
							Lua = {
								-- make the language server recognize "vim" global
								diagnostics = {
									globals = { "vim" },
								},
								completion = {
									callSnippet = "Replace",
								},
							},
						},
					})
				end,
			})
		end,
	},

	-- JAVA jdtls settings
	{
		"mfussenegger/nvim-jdtls",
		ft = "java",
		dependencies = { "williamboman/mason-lspconfig.nvim" },
		config = function()
			local jdtls = require("jdtls")
			local mason_registry = require("mason-registry")

			local function java_on_attach(_, bufnr)
				local opts = { buffer = bufnr, noremap = true, silent = true }

				vim.keymap.set("n", "crV", function()
					jdtls.extract_variable()
				end, opts)
				vim.keymap.set("n", "crC", function()
					jdtls.extract_constant()
				end, opts)
				vim.keymap.set("x", "crM", function()
					jdtls.extract_method(true)
				end, opts)

				vim.keymap.set("n", "<leader>tt", function()
					jdtls.test_nearest_method()
				end, opts)
				vim.keymap.set("n", "<leader>tT", function()
					jdtls.test_class()
				end, opts)

				vim.keymap.set("n", "<leader>lR", ":LspRestart<CR>", opts)

				jdtls.setup_dap({ hotcodereplace = "auto" })
				require("jdtls.dap").setup_dap_main_class_configs()
			end

			mason_registry.refresh(function()
				local pkg = mason_registry.get_package("jdtls")
				if not (pkg and pkg:is_installed()) then
					vim.notify("jdtls is not installed", vim.log.levels.ERROR)
					return
				end

				local base = vim.fn.stdpath("data") .. "/mason/packages"
				local jdtls_path = base .. "/jdtls"
				local java_test_path = base .. "/java-test"
				local dbg_path = base .. "/java-debug-adapter"

				local test_bundle = vim.split(vim.fn.glob(java_test_path .. "/extension/server/*.jar", true), "\n")
				local dbg_bundle = vim.split(
					vim.fn.glob(dbg_path .. "/extension/server/com.microsoft.java.debug.plugin-*.jar", true),
					"\n"
				)
				local bundles = {}
				vim.list_extend(bundles, test_bundle)
				vim.list_extend(bundles, dbg_bundle)

				local project_name = vim.fn.fnamemodify(vim.fn.getcwd(), ":p:h:t")
				local workspace_dir = vim.fn.stdpath("data") .. "/site/java/workspace-root/" .. project_name
				local root_dir = require("jdtls.setup").find_root({
					".git",
					"mvnw",
					"gradlew",
					"pom.xml",
					"build.gradle",
				})
				if not root_dir then
					return
				end

				local config = {
					cmd = {
						"java",
						"-Declipse.application=org.eclipse.jdt.ls.core.id1",
						"-Dosgi.bundles.defaultStartLevel=4",
						"-Declipse.product=org.eclipse.jdt.ls.core.product",
						"-Dlog.protocol=true",
						"-Dlog.level=ALL",
						"-javaagent:" .. jdtls_path .. "/lombok.jar",
						"-Xms1g",
						"--add-modules=ALL-SYSTEM",
						"--add-opens=java.base/java.util=ALL-UNNAMED",
						"--add-opens=java.base/java.lang=ALL-UNNAMED",
						"-jar",
						vim.fn.glob(jdtls_path .. "/plugins/org.eclipse.equinox.launcher_*.jar"),
						"-configuration",
						jdtls_path .. "/config_mac",
						"-data",
						workspace_dir,
					},
					root_dir = root_dir,
					on_attach = java_on_attach,
					settings = {
						java = {
							signatureHelp = { enabled = true },
							contentProvider = { preferred = "fernflower" },
						},
					},
					init_options = { bundles = bundles },
				}

				jdtls.start_or_attach(config)
			end)

			vim.api.nvim_create_autocmd("FileType", {
				pattern = "java",
				callback = function()
					local opts = { noremap = true, silent = true }
					vim.keymap.set("n", "<leader>gr", "<cmd>!./gradlew :app:run<CR>", opts)
					vim.keymap.set("n", "<leader>gb", "<cmd>!./gradlew build<CR>", opts)
				end,
			})
		end,
	},
}
