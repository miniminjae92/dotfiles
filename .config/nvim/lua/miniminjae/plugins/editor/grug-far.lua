-- 프로젝트 전역 찾아 바꾸기. 결과를 버퍼에서 확인하고 고른 것만 적용한다(무턱대고 :%s 하지 않으려는 것).
return {
	"MagicDuck/grug-far.nvim",
	cmd = "GrugFar",
	opts = { headerMaxWidth = 80 },
	keys = {
		{
			"<leader>sr",
			function()
				require("grug-far").open()
			end,
			desc = "전역 찾아 바꾸기",
		},
		{
			"<leader>sw",
			function()
				require("grug-far").open({ prefills = { search = vim.fn.expand("<cword>") } })
			end,
			desc = "커서 단어 전역 바꾸기",
		},
	},
}
