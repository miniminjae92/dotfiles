-- set leader key to space
vim.g.mapleader = " "

local keymap = vim.keymap -- for conciseness

---------------------
-- General Keymaps -------------------

-- indent
keymap.set("v", "<", "<gv", { desc = "Continue Left Indent" })
keymap.set("v", ">", ">gv", { desc = "Continue Right Indent" })

-- paste all
keymap.set("n", "<leader>gg", "ggVGy", { desc = "Copy entire line" })
keymap.set("n", "<S-k>", "yyp", { desc = "Duplicate line below" })
keymap.set("n", "<leader>aa", "GVgg", { desc = "Duplicate line below" })

-- use jk to exit insert mode
keymap.set("i", "jk", "<ESC>", { desc = "Exit insert mode with jk" })

-- clear search highlights
keymap.set("n", "<leader>h", ":nohl<CR>", { desc = "Clear search highlights" })

-- delete single character without copying into register
-- keymap.set("n", "x", '"_x')

-- window management
keymap.set("n", "<leader>sv", "<C-w>v", { desc = "Split window vertically" }) -- split window vertically
keymap.set("n", "<leader>sh", "<C-w>s", { desc = "Split window horizontally" }) -- split window horizontally
keymap.set("n", "<leader>se", "<C-w>=", { desc = "Make splits equal size" }) -- make split windows equal width & height
keymap.set("n", "<leader>sx", "<cmd>close<CR>", { desc = "Close current split" }) -- close current split window

keymap.set("n", "<leader>to", "<cmd>tabnew<CR>", { desc = "Open new tab" }) -- open new tab
keymap.set("n", "<leader>tx", "<cmd>tabclose<CR>", { desc = "Close current tab" }) -- close current tab
keymap.set("n", "<leader>tn", "<cmd>tabn<CR>", { desc = "Go to next tab" }) --  go to next tab
keymap.set("n", "<leader>tp", "<cmd>tabp<CR>", { desc = "Go to previous tab" }) --  go to previous tab
keymap.set("n", "<leader>tf", "<cmd>tabnew %<CR>", { desc = "Open current buffer in new tab" }) --  move current buffer to new tab

vim.api.nvim_create_autocmd("FileType", {
	pattern = { "markdown", "mdx" },
	callback = function()
		-- Visual 모드: nvim-surround의 'S' 기능을 이용해 **로 감싸기
		-- remap = true 필수 (S가 플러그인 매핑이기 때문)
		keymap.set("v", "<leader>b", 'c**<C-r>"**<Esc>', { desc = "선택 영역 Bold 처리" })

		-- Normal 모드: 현재 단어 볼드 처리 (단어 위에서 Ctrl+b)
		keymap.set("n", "<leader>b", "bi**<Esc>ea**<Esc>", { buffer = true, desc = "Bold Word" })
	end,
})

keymap.set({ "n", "i" }, "<leader>;", function()
	-- 1. cosco 플러그인 함수 호출 (세미콜론 or 콤마 자동 부착)
	-- (플러그인이 로드 안 됐을 경우를 대비해 pcall 사용)
	local status, _ = pcall(vim.fn["cosco#commaOrSemiColon"])

	if not status then
		-- 혹시 cosco가 없으면 그냥 기본적인 세미콜론 붙이기 시도 (비상용)
		vim.cmd("normal! A;")
	end

	-- 2. 저장하고 다음 줄로 개행 (인텔리제이처럼)
	-- <Esc>로 노멀모드 -> o로 다음 줄 생성
	local keys = vim.api.nvim_replace_termcodes("<Esc>o", true, false, true)
	vim.api.nvim_feedkeys(keys, "n", false)
end, { desc = "Complete Statement (Cosco + Newline)" })

-- [Smart New Line]
-- 인텔리제이의 Shift + Enter 기능 (세미콜론 없이 다음 줄로 개행)
-- Insert 모드에서 커서가 문장 중간에 있어도, 글자를 자르지 않고 아래에 새 줄을 만듭니다.
keymap.set({ "i" }, "<leader>o", function()
	-- <Esc>로 노멀 모드로 갔다가 -> o (아래에 줄 삽입 및 Insert 모드 진입)
	local keys = vim.api.nvim_replace_termcodes("<Esc>o", true, false, true)
	vim.api.nvim_feedkeys(keys, "n", false)
end, { desc = "Smart New Line (No Semicolon)" })
