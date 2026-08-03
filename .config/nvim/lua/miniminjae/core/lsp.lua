-- LSP를 "켜는" 층. nvim 0.11+ 네이티브 방식만 쓴다: lsp/<서버>.lua 로 설정하고 vim.lsp.enable로 켠다.
-- jdtls는 여기 없다 — 프로젝트 루트를 버퍼마다 새로 계산해야 해서 ftplugin/java.lua가 전담한다.

-- 0.11부터 virtual_text가 기본 off라 명시적으로 되살린다. signs는 severity를 키로 받는 새 형식.
vim.diagnostic.config({
	severity_sort = true,
	virtual_text = { spacing = 2, source = "if_many" },
	signs = {
		text = {
			[vim.diagnostic.severity.ERROR] = "",
			[vim.diagnostic.severity.WARN] = "",
			[vim.diagnostic.severity.HINT] = "󰠠",
			[vim.diagnostic.severity.INFO] = "",
		},
	},
	float = { border = "rounded", source = "if_many" },
})

-- lsp/<서버>.lua를 최우선 슬롯에 다시 올린다.
-- rtp에 있는 같은 이름 파일은 나중 것이 이기는데, nvim-lspconfig가 우리 뒤에 오므로
-- 파일만 두면 기본값에 덮인다. vim.lsp.config() 호출은 rtp 병합보다 우선순위가 높다.
for _, path in ipairs(vim.fn.glob(vim.fn.stdpath("config") .. "/lsp/*.lua", true, true)) do
	vim.lsp.config(vim.fn.fnamemodify(path, ":t:r"), dofile(path))
end

-- 완성 엔진이 지원하는 기능(스니펫·추가 텍스트 편집 등)을 모든 서버에 알린다.
-- 이게 빠지면 완성으로 클래스를 고를 때 import가 자동으로 안 붙는다.
vim.lsp.config("*", { capabilities = require("blink.cmp").get_lsp_capabilities(nil, true) })

vim.lsp.enable({
	"lua_ls",
	"ts_ls",
	"html",
	"cssls",
	"tailwindcss",
	"svelte",
	"graphql",
	"emmet_ls",
	"pyright",
	"marksman",
	"mdx_analyzer",
	"clangd",
	"jsonls",
	"yamlls",
})

-- 이동 계열은 결과가 여러 개일 때 목록이 필요하다. fzf-lua가 있으면 피커로, 없으면 내장으로 떨어진다.
-- (core 층이 UI 플러그인에 강제로 매이지 않게 하려는 의도)
local function pick(picker, builtin)
	return function()
		local ok, fzf = pcall(require, "fzf-lua")
		if ok then
			fzf[picker]()
		else
			builtin()
		end
	end
end

vim.api.nvim_create_autocmd("LspAttach", {
	group = vim.api.nvim_create_augroup("miniminjae_lsp_attach", { clear = true }),
	callback = function(ev)
		local function map(mode, lhs, rhs, desc)
			vim.keymap.set(mode, lhs, rhs, { buffer = ev.buf, silent = true, desc = desc })
		end

		map("n", "gd", pick("lsp_definitions", vim.lsp.buf.definition), "정의로")
		map("n", "gD", vim.lsp.buf.declaration, "선언으로")
		map("n", "gR", pick("lsp_references", vim.lsp.buf.references), "참조 목록")
		map("n", "gi", pick("lsp_implementations", vim.lsp.buf.implementation), "구현 목록")
		map("n", "gt", pick("lsp_typedefs", vim.lsp.buf.type_definition), "타입 정의")
		map("n", "gh", vim.lsp.buf.hover, "문서 보기")
		map({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, "코드 액션")
		map("n", "<leader>rn", vim.lsp.buf.rename, "이름 바꾸기")
		map("n", "<leader>rs", "<cmd>LspRestart<CR>", "LSP 재시작")

		-- 인레이 힌트는 지원하는 서버에서만. 기본 on/off는 언어별 설정이 정한다.
		local client = vim.lsp.get_client_by_id(ev.data.client_id)
		if client and client:supports_method("textDocument/inlayHint") then
			map("n", "<leader>ch", function()
				vim.lsp.inlay_hint.enable(not vim.lsp.inlay_hint.is_enabled({ bufnr = ev.buf }), { bufnr = ev.buf })
			end, "인레이 힌트 토글")
		end
	end,
})
