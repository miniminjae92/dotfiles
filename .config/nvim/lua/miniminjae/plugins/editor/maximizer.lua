-- 분할 하나를 잠깐 전체 화면으로. 디버깅 중 좁아진 코드 창을 넓힐 때 쓴다.
return {
	"szw/vim-maximizer",
	keys = {
		{ "<leader>sm", "<cmd>MaximizerToggle<CR>", desc = "분할 최대화 토글" },
	},
}
