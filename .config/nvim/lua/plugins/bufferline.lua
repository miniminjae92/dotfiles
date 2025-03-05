local mapKey = require("utils.keyMapper").mapKey

return {
	"akinsho/bufferline.nvim",
	version = "*",
	dependencies = "nvim-tree/nvim-web-devicons",
	config = function()
		require("bufferline").setup({})

		mapKey("<Tab>", "<cmd>BufferLineCycleNext<CR>")
		mapKey("<S-Tab>", "<cmd>BufferLineCyclePrev<CR>")
		mapKey("<leader>q", "<cmd>bd<CR>")
	end,
}
