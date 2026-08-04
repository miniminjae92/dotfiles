-- 진단·quickfix·TODO를 한 창에 모아 훑는다. 흩어진 경고를 순회할 때 쓴다.
return {
	"folke/trouble.nvim",
	dependencies = { "nvim-tree/nvim-web-devicons", "folke/todo-comments.nvim" },
	cmd = "Trouble",
	opts = { focus = true },
	keys = {
		{ "<leader>xw", "<cmd>Trouble diagnostics toggle<CR>", desc = "프로젝트 진단" },
		{ "<leader>xd", "<cmd>Trouble diagnostics toggle filter.buf=0<CR>", desc = "이 파일 진단" },
		{ "<leader>xq", "<cmd>Trouble quickfix toggle<CR>", desc = "quickfix 목록" },
		{ "<leader>xl", "<cmd>Trouble loclist toggle<CR>", desc = "location 목록" },
		{ "<leader>xt", "<cmd>Trouble todo toggle<CR>", desc = "TODO 목록" },
	},
}
