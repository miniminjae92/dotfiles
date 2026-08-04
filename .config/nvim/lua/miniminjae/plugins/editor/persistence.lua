-- 디렉터리별로 열어 둔 창 배치를 기억한다. 자동 복원은 하지 않는다 — 돌아올 때 직접 부른다.
return {
	"folke/persistence.nvim",
	event = "BufReadPre",
	opts = {},
	keys = {
		{
			"<leader>wr",
			function()
				require("persistence").load()
			end,
			desc = "이 디렉터리 세션 복원",
		},
		{
			"<leader>wl",
			function()
				require("persistence").load({ last = true })
			end,
			desc = "마지막 세션 복원",
		},
		{
			"<leader>ws",
			function()
				require("persistence").save()
			end,
			desc = "세션 저장",
		},
		{
			"<leader>wd",
			function()
				require("persistence").stop()
			end,
			desc = "이번 세션은 저장 안 함",
		},
	},
}
