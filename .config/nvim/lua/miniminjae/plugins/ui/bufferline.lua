-- 상단 탭 줄. 버퍼가 아니라 탭 단위로 보여준다(작업 묶음 = 탭이라는 사용 습관에 맞춘 것).
return {
	"akinsho/bufferline.nvim",
	dependencies = { "nvim-tree/nvim-web-devicons" },
	version = "*",
	event = "VeryLazy",
	opts = {
		options = {
			mode = "tabs",
			separator_style = "slant",
		},
	},
}
