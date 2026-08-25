-- 화면 밖으로 밀린 함수, 컴포넌트, JSX 조상을 위에 고정해 현재 코드의 바깥 문맥을 보존한다.
return {
	"nvim-treesitter/nvim-treesitter-context",
	event = { "BufReadPost", "BufNewFile" },
	opts = {
		max_lines = 1,
		multiline_threshold = 2,
		trim_scope = "inner",
		mode = "cursor",
	},
	keys = {
		{
			"<leader>cu",
			function()
				require("treesitter-context").go_to_context(vim.v.count1)
			end,
			desc = "현재 바깥 스코프로 이동",
		},
	},
}
