-- 파일 조작을 "버퍼 편집"으로 한다. 이름 바꾸기·옮기기·지우기를 vim 편집 그대로 하고 :w로 확정한다.
-- 트리(snacks.explorer)와 병행: 훑어보기는 트리, 손대기는 oil.
return {
	"stevearc/oil.nvim",
	dependencies = { "nvim-tree/nvim-web-devicons" },
	lazy = false,
	opts = {
		default_file_explorer = true,
		delete_to_trash = true,
		view_options = { show_hidden = true },
	},
	keys = {
		{ "-", "<cmd>Oil<cr>", desc = "상위 폴더 열기 (oil)" },
	},
}
