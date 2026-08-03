-- 파일종류에 따라붙는 규칙. 특정 언어 전용 로직은 ftplugin/으로 뺀다.

local augroup = vim.api.nvim_create_augroup("miniminjae_core", { clear = true })

-- 마크다운 계열에서만 볼드 토글. buffer=true를 붙여 다른 파일로 새지 않게 한다.
vim.api.nvim_create_autocmd("FileType", {
	group = augroup,
	pattern = { "markdown", "mdx" },
	callback = function(ev)
		vim.keymap.set("v", "<leader>b", 'c**<C-r>"**<Esc>', { buffer = ev.buf, desc = "선택 영역 볼드" })
		vim.keymap.set("n", "<leader>b", "bi**<Esc>ea**<Esc>", { buffer = ev.buf, desc = "현재 단어 볼드" })
	end,
})
