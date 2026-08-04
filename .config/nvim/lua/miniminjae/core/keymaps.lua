-- 전역 키맵. 플러그인 키맵은 각 플러그인 스펙에, LSP 키맵은 core/lsp.lua에 둔다.
-- leader는 lazy보다 먼저 정해져야 플러그인 keys 정의가 올바르게 잡힌다.
vim.g.mapleader = " "
vim.g.maplocalleader = " "

local keymap = vim.keymap

-- 들여쓰기 후에도 선택을 유지
keymap.set("v", "<", "<gv", { desc = "선택 유지하며 왼쪽 들여쓰기" })
keymap.set("v", ">", ">gv", { desc = "선택 유지하며 오른쪽 들여쓰기" })

-- 파일 전체 다루기
keymap.set("n", "<leader>gg", "ggVGy", { desc = "파일 전체 복사" })
keymap.set("n", "<leader>aa", "GVgg", { desc = "파일 전체 선택" })
keymap.set("n", "<S-k>", "yyp", { desc = "현재 줄 아래로 복제" })

keymap.set("i", "jk", "<ESC>", { desc = "삽입 모드 나가기" })
keymap.set("n", "<leader>hh", "<cmd>nohl<CR>", { desc = "검색 하이라이트 지우기" })

-- 창 분할
keymap.set("n", "<leader>sv", "<C-w>v", { desc = "세로 분할" })
keymap.set("n", "<leader>sh", "<C-w>s", { desc = "가로 분할" })
keymap.set("n", "<leader>se", "<C-w>=", { desc = "분할 크기 균등" })
keymap.set("n", "<leader>sx", "<cmd>close<CR>", { desc = "현재 분할 닫기" })

-- 탭
keymap.set("n", "<leader>to", "<cmd>tabnew<CR>", { desc = "새 탭" })
keymap.set("n", "<leader>tx", "<cmd>tabclose<CR>", { desc = "탭 닫기" })
keymap.set("n", "<leader>tn", "<cmd>tabn<CR>", { desc = "다음 탭" })
keymap.set("n", "<leader>tp", "<cmd>tabp<CR>", { desc = "이전 탭" })
keymap.set("n", "<leader>tf", "<cmd>tabnew %<CR>", { desc = "현재 버퍼를 새 탭으로" })

-- 진단은 LSP 없이도(nvim-lint 등) 생기므로 LspAttach가 아니라 전역에 둔다.
-- `<leader>d`는 디버그 그룹에 양보했고, 줄 진단은 `gl`이 맡는다.
keymap.set("n", "gl", vim.diagnostic.open_float, { desc = "줄 진단 띄우기" })
keymap.set("n", "]d", function()
	vim.diagnostic.jump({ count = 1, float = true })
end, { desc = "다음 진단" })
keymap.set("n", "[d", function()
	vim.diagnostic.jump({ count = -1, float = true })
end, { desc = "이전 진단" })

-- [IntelliJ Ctrl+Shift+Enter] 문장 완성: cosco가 `;`/`,`를 판단해 붙이고 다음 줄로 내려간다.
keymap.set({ "n", "i" }, "<leader>;", function()
	local ok = pcall(vim.fn["cosco#commaOrSemiColon"])
	if not ok then
		vim.cmd("normal! A;")
	end
	local keys = vim.api.nvim_replace_termcodes("<Esc>o", true, false, true)
	vim.api.nvim_feedkeys(keys, "n", false)
end, { desc = "문장 완성 후 개행 (cosco)" })

-- [IntelliJ Shift+Enter] 커서 위치와 무관하게 아래에 새 줄
keymap.set({ "n", "i" }, "<leader>:", function()
	local keys = vim.api.nvim_replace_termcodes("<Esc>o", true, false, true)
	vim.api.nvim_feedkeys(keys, "n", false)
end, { desc = "아래에 새 줄 (세미콜론 없이)" })
