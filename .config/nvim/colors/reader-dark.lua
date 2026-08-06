-- reader-dark: Ghostty 전용 자작 테마.
-- 팔레트 정본은 assets/markdown-reader.css의 [data-theme="dark"] 블록이다. 수정 시 함께 고칠 것.
-- 파생색(red, diff 배경)과 ANSI 16색은 .config/ghostty/themes/reader-dark와 동일하게 유지한다.
-- 배경은 투명(터미널 bg #1d2224가 canvas 역할), 떠 있는 창만 surface를 깐다.
local p = {
	canvas = "#1d2224",
	surface = "#252b2d",
	subtle = "#30383a",
	table_header = "#343d3f",
	border = "#485154",
	code_bg = "#171b1c",
	text = "#e7dfd2",
	muted = "#b6ada0",
	heading = "#f4eddf",
	code_text = "#eee7dc",
	accent = "#e29a68",
	inline_code = "#f0bb8d",
	link = "#7fc6dd",
	link_hover = "#b1e0ed",
	comment = "#9ba5a8",
	keyword = "#d7a3df",
	number = "#f0bd73",
	string = "#a9d68d",
	type = "#82c7de",
	meta = "#e8c77c",
	symbol = "#e1a6c8",
	red = "#d47f77", -- 파생 테라코타(정본에 빨강 없음), 터미널 ANSI 1과 동일
	-- diff 배경: 색을 canvas 위에 20% 얹은 정적 블렌드(0.2*color + 0.8*canvas)
	diff_add_bg = "#394639",
	diff_change_bg = "#474134",
	diff_delete_bg = "#423535",
}

vim.cmd("highlight clear")
vim.g.colors_name = "reader-dark"

local function hl(group, spec)
	vim.api.nvim_set_hl(0, group, spec)
end
local NONE = "NONE"

-- ── 에디터 크롬 ──────────────────────────────────────────────
hl("Normal", { fg = p.text, bg = NONE })
hl("NormalNC", { fg = p.text, bg = NONE })
hl("NormalFloat", { fg = p.text, bg = p.surface })
hl("FloatBorder", { fg = p.border, bg = p.surface })
hl("FloatTitle", { fg = p.heading, bg = p.surface, bold = true })
hl("Pmenu", { fg = p.text, bg = p.surface })
hl("PmenuSel", { bg = p.subtle, bold = true })
hl("PmenuSbar", { bg = p.subtle })
hl("PmenuThumb", { bg = p.border })
hl("CursorLine", { bg = p.surface })
hl("CursorColumn", { bg = p.surface })
hl("ColorColumn", { bg = p.surface })
hl("CursorLineNr", { fg = p.heading, bold = true })
hl("LineNr", { fg = p.border })
hl("SignColumn", { bg = NONE })
hl("Visual", { bg = p.subtle })
hl("Search", { fg = p.canvas, bg = p.accent })
hl("CurSearch", { fg = p.code_bg, bg = p.inline_code, bold = true })
hl("IncSearch", { link = "CurSearch" })
hl("MatchParen", { fg = p.inline_code, bg = p.subtle, bold = true })
hl("StatusLine", { fg = p.text, bg = p.table_header })
hl("StatusLineNC", { fg = p.muted, bg = p.surface })
hl("WinSeparator", { fg = p.border, bg = NONE })
hl("WinBar", { fg = p.heading, bg = NONE, bold = true })
hl("WinBarNC", { fg = p.muted, bg = NONE })
hl("TabLine", { fg = p.muted, bg = p.surface })
hl("TabLineSel", { fg = p.heading, bg = NONE, bold = true })
hl("TabLineFill", { bg = NONE })
hl("Folded", { fg = p.muted, bg = p.surface })
hl("FoldColumn", { fg = p.border, bg = NONE })
hl("NonText", { fg = p.border })
hl("Whitespace", { fg = p.subtle })
hl("SpecialKey", { fg = p.border })
hl("EndOfBuffer", { fg = p.canvas, bg = NONE })
hl("QuickFixLine", { bg = p.subtle })
hl("Directory", { fg = p.link })
hl("Title", { fg = p.heading, bold = true })
hl("ErrorMsg", { fg = p.red })
hl("WarningMsg", { fg = p.number })
hl("MoreMsg", { fg = p.string })
hl("Question", { fg = p.link })
hl("SpellBad", { undercurl = true, sp = p.red })
hl("SpellCap", { undercurl = true, sp = p.number })
hl("SpellLocal", { undercurl = true, sp = p.link })
hl("SpellRare", { undercurl = true, sp = p.symbol })

-- ── 문법(legacy 기본 그룹; @그룹 대부분이 여기로 링크된다) ───
hl("Comment", { fg = p.comment, italic = true })
hl("String", { fg = p.string })
hl("Character", { fg = p.string })
hl("Number", { fg = p.number })
hl("Float", { fg = p.number })
hl("Boolean", { fg = p.number })
hl("Constant", { fg = p.number })
hl("Identifier", { fg = p.text })
hl("Function", { fg = p.type }) -- CSS의 syntax-title이 함수/클래스명 자리
hl("Statement", { fg = p.keyword })
hl("Keyword", { fg = p.keyword })
hl("Conditional", { fg = p.keyword })
hl("Repeat", { fg = p.keyword })
hl("Operator", { fg = p.muted })
hl("Type", { fg = p.type })
hl("StorageClass", { fg = p.keyword })
hl("Structure", { fg = p.type })
hl("Special", { fg = p.meta })
hl("SpecialChar", { fg = p.symbol })
hl("Delimiter", { fg = p.muted })
hl("PreProc", { fg = p.meta })
hl("Include", { fg = p.keyword })
hl("Macro", { fg = p.meta })
hl("Tag", { fg = p.type })
hl("Todo", { fg = p.canvas, bg = p.accent, bold = true })
hl("Error", { fg = p.red })
hl("Underlined", { fg = p.link, underline = true })

-- ── treesitter @그룹(기본 링크와 다른 것만) ──────────────────
hl("@variable", { fg = p.text })
hl("@variable.builtin", { fg = p.meta, italic = true })
hl("@variable.parameter", { fg = p.text, italic = true })
hl("@variable.member", { fg = p.code_text })
hl("@property", { fg = p.code_text })
hl("@constant.builtin", { fg = p.meta })
hl("@function.builtin", { fg = p.meta })
hl("@constructor", { fg = p.type })
hl("@type.builtin", { fg = p.meta })
hl("@module", { fg = p.text })
hl("@punctuation.bracket", { fg = p.muted })
hl("@punctuation.delimiter", { fg = p.muted })
hl("@punctuation.special", { fg = p.symbol })
hl("@string.escape", { fg = p.symbol })
hl("@string.regexp", { fg = p.meta })
hl("@tag", { fg = p.type })
hl("@tag.attribute", { fg = p.meta })
hl("@tag.delimiter", { fg = p.muted })
hl("@label", { fg = p.symbol })

-- ── 마크다운/@markup(render-markdown이 이 위에 얹힌다) ───────
hl("@markup.heading", { fg = p.heading, bold = true })
hl("@markup.strong", { fg = p.heading, bold = true })
hl("@markup.italic", { italic = true })
hl("@markup.strikethrough", { strikethrough = true })
hl("@markup.link", { fg = p.link })
hl("@markup.link.label", { fg = p.link })
hl("@markup.link.url", { fg = p.link, underline = true })
hl("@markup.raw", { fg = p.inline_code, bg = p.subtle })
hl("@markup.raw.block", { fg = p.code_text })
hl("@markup.quote", { fg = p.muted, italic = true })
hl("@markup.list", { fg = p.muted })
hl("@markup.list.checked", { fg = p.string })
hl("@markup.list.unchecked", { fg = p.muted })

-- ── 진단/LSP ─────────────────────────────────────────────────
hl("DiagnosticError", { fg = p.red })
hl("DiagnosticWarn", { fg = p.number })
hl("DiagnosticInfo", { fg = p.link })
hl("DiagnosticHint", { fg = p.comment })
hl("DiagnosticOk", { fg = p.string })
hl("DiagnosticUnderlineError", { undercurl = true, sp = p.red })
hl("DiagnosticUnderlineWarn", { undercurl = true, sp = p.number })
hl("DiagnosticUnderlineInfo", { undercurl = true, sp = p.link })
hl("DiagnosticUnderlineHint", { undercurl = true, sp = p.comment })
hl("LspReferenceText", { bg = p.subtle })
hl("LspReferenceRead", { bg = p.subtle })
hl("LspReferenceWrite", { bg = p.subtle, underline = true })
hl("LspInlayHint", { fg = p.comment, bg = p.code_bg })
hl("LspSignatureActiveParameter", { fg = p.inline_code, bold = true })

-- ── diff / git ───────────────────────────────────────────────
hl("DiffAdd", { bg = p.diff_add_bg })
hl("DiffChange", { bg = p.diff_change_bg })
hl("DiffDelete", { bg = p.diff_delete_bg })
hl("DiffText", { bg = p.subtle, bold = true })
hl("Added", { fg = p.string }) -- gitsigns 기본 링크의 종점
hl("Changed", { fg = p.meta })
hl("Removed", { fg = p.red })
hl("GitSignsAdd", { fg = p.string })
hl("GitSignsChange", { fg = p.meta })
hl("GitSignsDelete", { fg = p.red })

-- ── 플러그인 ─────────────────────────────────────────────────
-- mdview(markdown-reader.css)와 같은 색 경제: 본문은 크림, 유채색은 코드 필과
-- 링크에만 아껴 쓴다. 헤딩 바는 전부 끈다. 주의: bg=NONE 정의는 "클리어"로
-- 취급돼 플러그인의 default 링크(H3Bg->DiffChange 등)가 되살아나므로 canvas를 명시한다.
hl("RenderMarkdownCode", { bg = p.code_bg })
hl("RenderMarkdownCodeInline", { fg = p.inline_code, bg = p.subtle })
hl("RenderMarkdownBullet", { fg = p.muted })
hl("RenderMarkdownTableHead", { fg = p.border })
hl("RenderMarkdownTableRow", { fg = p.border })
hl("RenderMarkdownDash", { fg = p.border })
hl("RenderMarkdownQuote", { fg = p.muted, italic = true })
hl("RenderMarkdownLink", { fg = p.link })
for i = 1, 6 do
	hl("RenderMarkdownH" .. i .. "Bg", { bg = p.canvas })
end
hl("SnacksIndent", { fg = p.subtle })
hl("SnacksIndentScope", { fg = p.border })
hl("SnacksDashboardHeader", { fg = p.accent })
hl("SnacksDashboardKey", { fg = p.inline_code })
hl("SnacksDashboardIcon", { fg = p.link })
hl("SnacksDashboardDesc", { fg = p.text })
hl("SnacksDashboardFooter", { fg = p.muted })
hl("BlinkCmpLabelMatch", { fg = p.inline_code, bold = true })

-- ── :terminal(snacks lazygit·터미널이 쓴다) — ANSI 테마와 동일 ─
local ansi = {
	"#171b1c", "#d47f77", "#a9d68d", "#e8c77c", "#82c7de", "#d7a3df", "#7fc6dd", "#e7dfd2",
	"#707a7d", "#e09a93", "#bce3a4", "#f0bd73", "#a3d6e8", "#e1a6c8", "#b1e0ed", "#f4eddf",
}
for i, c in ipairs(ansi) do
	vim.g["terminal_color_" .. (i - 1)] = c
end
