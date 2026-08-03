-- leader를 누른 뒤 뭘 누를지 잊었을 때의 안전망. 그룹 이름은 이 설정의 지도 역할을 한다.
return {
	"folke/which-key.nvim",
	event = "VeryLazy",
	opts = {
		spec = {
			{ "<leader>c", group = "코드 (포맷·액션·인레이)" },
			{ "<leader>d", group = "디버그" },
			{ "<leader>e", group = "탐색기" },
			{ "<leader>f", group = "찾기" },
			{ "<leader>h", group = "git 헝크" },
			{ "<leader>j", group = "자바" },
			{ "<leader>k", group = "HTTP (kulala)" },
			{ "<leader>m", group = "마크다운" },
			{ "<leader>o", group = "옵시디언" },
			{ "<leader>r", group = "이름 바꾸기·재시작" },
			{ "<leader>s", group = "창 분할·치환" },
			{ "<leader>t", group = "탭·토글" },
			{ "<leader>T", group = "테스트" },
			{ "<leader>w", group = "세션" },
			{ "<leader>x", group = "진단 목록" },
		},
	},
	keys = {
		{
			"<leader>?",
			function()
				require("which-key").show({ global = false })
			end,
			desc = "이 버퍼의 키맵 보기",
		},
	},
}
