-- lazy.nvim 부트스트랩과 스펙 수집. 여러 기기에서 같은 상태를 재현하려고 lockfile을 쓴다.
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.uv.fs_stat(lazypath) then
	vim.fn.system({
		"git",
		"clone",
		"--filter=blob:none",
		"https://github.com/folke/lazy.nvim.git",
		"--branch=stable",
		lazypath,
	})
end
vim.opt.rtp:prepend(lazypath)

-- 층위별로 디렉터리를 나눠 둔다: ui(보이는 것) / editor(움직이는 것) / coding(쓰는 것) / lang(언어별)
require("lazy").setup({
	{ import = "miniminjae.plugins" },
	{ import = "miniminjae.plugins.ui" },
	{ import = "miniminjae.plugins.editor" },
	{ import = "miniminjae.plugins.coding" },
	{ import = "miniminjae.plugins.lang" },
}, {
	install = { colorscheme = { "solarized-osaka", "habamax" } },
	-- 여기 쓰는 플러그인 중 luarocks가 필요한 것이 없다. 켜 두면 hererocks를 못 찾는다고 계속 경고한다.
	rocks = { enabled = false },
	checker = { enabled = true, notify = false },
	change_detection = { notify = false },
	ui = { border = "rounded" },
})
