-- 코드를 문법 트리로 읽어 색·들여쓰기·선택 범위를 정확히 잡는 층.
-- main 브랜치는 master와 API가 완전히 다르다: setup()이 하이라이팅을 켜주지 않고,
-- 파서 설치(install)와 켜기(vim.treesitter.start)를 우리가 직접 한다. 파서 컴파일에 tree-sitter CLI가 필요하다.
local parsers = {
	-- 웹·프론트엔드
	"javascript",
	"typescript",
	"tsx",
	"html",
	"css",
	"svelte",
	"graphql",
	"prisma",
	-- 데이터·설정
	"json",
	"yaml",
	"dockerfile",
	"gitignore",
	-- 문서
	"markdown",
	"markdown_inline",
	"mermaid", -- ERD·UML 정본 표기법
	-- 시스템·에디터
	"bash",
	"lua",
	"vim",
	"vimdoc",
	"query",
	-- 언어
	"c",
	"cpp",
	"java",
	-- 아래 둘은 Phase 7의 도구가 요구한다: kulala(.http), dadbod(SQL 콘솔)
	"http",
	"sql",
}

return {
	"nvim-treesitter/nvim-treesitter",
	branch = "main",
	lazy = false,
	build = ":TSUpdate",
	config = function()
		local ts = require("nvim-treesitter")

		ts.setup({})

		-- 없는 파서만 받아온다. 첫 실행은 컴파일 때문에 오래 걸리고, 그 뒤로는 즉시 끝난다.
		ts.install(parsers)

		-- master의 `highlight = { enable = true }` 자리를 대신하는 부분.
		vim.api.nvim_create_autocmd("FileType", {
			group = vim.api.nvim_create_augroup("miniminjae_treesitter", { clear = true }),
			callback = function(ev)
				local lang = vim.treesitter.language.get_lang(ev.match)
				if not lang then
					return
				end
				-- 파서가 아직 없으면 조용히 넘어간다(설치 중이거나 지원하지 않는 언어).
				if not pcall(vim.treesitter.start, ev.buf, lang) then
					return
				end
				-- 들여쓰기 규칙(indents.scm)이 있는 언어에만 treesitter 들여쓰기를 맡긴다.
				if vim.treesitter.query.get(lang, "indents") then
					vim.bo[ev.buf].indentexpr = "v:lua.require'nvim-treesitter'.indentexpr()"
				end
			end,
		})
	end,
}
