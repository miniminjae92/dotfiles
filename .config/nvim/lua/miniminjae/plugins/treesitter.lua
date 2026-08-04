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
	"python",
	-- 아래 둘은 Phase 7의 도구가 요구한다: kulala(.http), dadbod(SQL 콘솔)
	"http",
	"sql",
}

-- [IntelliJ Ctrl+W / Ctrl+Shift+W] 문법 단위로 선택을 넓히고 좁힌다.
-- .ideavimrc의 `<CR>`=EditorSelectWord, `<BS>`=EditorUnSelectWord 자리를 그대로 옮긴 것이다.
-- master에 있던 incremental_selection 모듈이 main에는 없어서 직접 만든다.

-- 넓혀온 범위를 버퍼별로 쌓아둔다. <BS>는 이 스택을 되감기만 하므로 축소가 확장의 정확한 역순이 된다.
-- 트리를 다시 내려가며 자식을 고르는 방식은 어느 자식으로 갈지가 모호해 되돌아오지 못한다.
local history = {}

-- treesitter 범위(0-indexed·끝 열 exclusive)를 커서 좌표(1-indexed·끝 열 포함)로 옮긴다.
local function to_cursor(buf, range)
	local srow, scol, erow, ecol = unpack(range)
	-- 노드가 줄 경계에서 끝나면 끝 열이 0으로 온다. 그대로 두면 다음 줄 첫 칸까지 잡힌다.
	if ecol == 0 and erow > srow then
		erow = erow - 1
		ecol = #vim.api.nvim_buf_get_lines(buf, erow, erow + 1, true)[1]
	end
	return srow + 1, scol + 1, erow + 1, ecol
end

-- 지금 비주얼 선택을 같은 좌표계로 돌려준다. 아래에서 위로 잡았으면 시작이 끝보다 뒤라 정렬한다.
local function visual_cursor()
	local a, b = vim.fn.getpos("v"), vim.fn.getpos(".")
	local sr, sc, er, ec = a[2], a[3], b[2], b[3]
	if sr > er or (sr == er and sc > ec) then
		sr, sc, er, ec = er, ec, sr, sc
	end
	return sr, sc, er, ec
end

local function in_visual()
	return vim.fn.mode():match("^[vV\22]") ~= nil
end

local function select_range(buf, range)
	local sr, sc, er, ec = to_cursor(buf, range)
	-- 이미 비주얼이면 한 번 빠져나와야 시작점을 다시 찍을 수 있다.
	if in_visual() then
		vim.cmd("normal! \27")
	end
	vim.fn.setpos(".", { buf, sr, sc, 0 })
	vim.cmd("normal! v")
	vim.fn.setpos(".", { buf, er, ec, 0 })
end

local function node_for_range(buf, range)
	local ok, parser = pcall(vim.treesitter.get_parser, buf)
	if not ok or not parser then
		return nil
	end
	return parser:named_node_for_range(range)
end

local function expand()
	local buf = vim.api.nvim_get_current_buf()

	-- 비주얼이 아니면 이어가던 선택이 아니다. 커서 아래 노드에서 새로 시작한다.
	if not in_visual() then
		local node = vim.treesitter.get_node()
		if not node then
			return
		end
		history[buf] = { { node:range() } }
		select_range(buf, history[buf][1])
		return
	end

	local stack = history[buf] or {}
	local sr, sc, er, ec = visual_cursor()
	local top = stack[#stack]
	-- 꼭대기가 지금 선택과 다르면 직접 잡은 범위이거나 예전 잔재다. 그 범위에서 새로 시작한다.
	if not top or not vim.deep_equal({ to_cursor(buf, top) }, { sr, sc, er, ec }) then
		stack = { { sr - 1, sc - 1, er - 1, ec } }
		history[buf] = stack
	end

	local current = stack[#stack]
	local node = node_for_range(buf, current)
	-- 같은 범위를 감싸는 노드가 겹겹이 있을 수 있어(래퍼 노드) 실제로 커지는 조상까지 올라간다.
	while node do
		local nr = { node:range() }
		if nr[1] ~= current[1] or nr[2] ~= current[2] or nr[3] ~= current[3] or nr[4] ~= current[4] then
			break
		end
		node = node:parent()
	end
	if not node then
		return -- 루트까지 왔다. 선택을 그대로 둔다.
	end

	local next_range = { node:range() }
	table.insert(stack, next_range)
	select_range(buf, next_range)
end

local function shrink()
	local buf = vim.api.nvim_get_current_buf()
	local stack = history[buf]
	if not stack or #stack < 2 then
		return
	end
	table.remove(stack)
	select_range(buf, stack[#stack])
end

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

				-- 파서가 실제로 붙은 일반 파일에만 건다. 도움말의 <CR>(태그 점프)이나
				-- quickfix의 <CR>(항목 열기)까지 빼앗지 않으려면 buftype을 봐야 한다.
				if vim.bo[ev.buf].buftype == "" then
					vim.keymap.set("n", "<CR>", expand, { buffer = ev.buf, desc = "선택을 문법 단위로 넓히기" })
					vim.keymap.set("x", "<CR>", expand, { buffer = ev.buf, desc = "선택을 문법 단위로 넓히기" })
					vim.keymap.set("x", "<BS>", shrink, { buffer = ev.buf, desc = "선택을 한 단계 좁히기" })
				end
			end,
		})
	end,
}
