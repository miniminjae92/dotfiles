return {
	"HakonHarnes/img-clip.nvim",
	event = "VeryLazy",
	opts = {
		-- add options here
		-- or leave it empty to use the default settings
		default = {
			-- 현재 파일과 같은 위치에 저장 (".")
			dir_path = ".",

			-- 파일명 생성 규칙
			file_name = "%Y-%m-%d-%H-%M-%S",

			-- 절대 경로 끄고, 상대 경로 켜기
			use_absolute_path = false,
			relative_to_current_file = true,
		},
	},
	keys = {
		-- suggested keymap
		{ "<leader>p", "<cmd>PasteImage<cr>", desc = "Paste image from system clipboard" },
	},
}
