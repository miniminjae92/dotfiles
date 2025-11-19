vim.api.nvim_create_autocmd({ "BufEnter", "BufRead" }, {
	pattern = { "*.mdx" },
	callback = function()
		vim.bo.filetype = "markdown"
	end,
})

require("miniminjae.core.options")
require("miniminjae.core.keymaps")
