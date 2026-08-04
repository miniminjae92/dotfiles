-- 변경분을 파일 단위로 나란히 놓고 읽는다. 에이전트가 만든 diff를 검토하는 자리가 여기다.
return {
	"sindrets/diffview.nvim",
	cmd = { "DiffviewOpen", "DiffviewClose", "DiffviewFileHistory", "DiffviewToggleFiles" },
	keys = {
		{ "<leader>gd", "<cmd>DiffviewOpen<cr>", desc = "작업 변경분 리뷰" },
		{ "<leader>gf", "<cmd>DiffviewFileHistory %<cr>", desc = "이 파일의 히스토리" },
		{ "<leader>gq", "<cmd>DiffviewClose<cr>", desc = "diffview 닫기" },
	},
}
