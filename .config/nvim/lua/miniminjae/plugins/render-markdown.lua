return {
	"MeanderingProgrammer/render-markdown.nvim",
	opts = {
		file_types = { "markdown", "mdx" }, -- mdx도 지원하도록 설정
		code = {
			sign = false,
			width = "block",
			right_pad = 1,
		},
		heading = {
			sign = false,
			icons = {}, -- # 기호 대신 깔끔하게 크기만 조절
		},
	},
	ft = { "markdown", "mdx" }, -- 파일 열 때 로드
}
