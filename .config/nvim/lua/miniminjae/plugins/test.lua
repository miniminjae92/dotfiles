-- 테스트 실행의 언어 무관 부분. 어댑터는 lang/<언어>.lua가 opts.adapters에 꽂는다.
-- 키가 문자열이면 모듈 이름으로 보고 require해서 붙인다(설정 테이블이 있으면 넘겨준다).
return {
	"nvim-neotest/neotest",
	dependencies = {
		"nvim-neotest/nvim-nio",
		"nvim-lua/plenary.nvim",
		"nvim-treesitter/nvim-treesitter",
	},
	opts = { adapters = {} },
	config = function(_, opts)
		local adapters = {}
		for name, config in pairs(opts.adapters or {}) do
			if type(name) == "number" then
				adapters[#adapters + 1] = config
			else
				local adapter = require(name)
				if type(config) == "table" and not vim.tbl_isempty(config) then
					adapter = adapter(config)
				end
				adapters[#adapters + 1] = adapter
			end
		end
		opts.adapters = adapters
		require("neotest").setup(opts)
	end,
	keys = {
		{
			"<leader>Tt",
			function()
				require("neotest").run.run()
			end,
			desc = "커서 근처 테스트 실행",
		},
		{
			"<leader>Tf",
			function()
				require("neotest").run.run(vim.fn.expand("%"))
			end,
			desc = "이 파일 테스트 실행",
		},
		{
			"<leader>Ta",
			function()
				require("neotest").run.run(vim.uv.cwd())
			end,
			desc = "프로젝트 전체 테스트",
		},
		{
			"<leader>Td",
			function()
				require("neotest").run.run({ strategy = "dap" })
			end,
			desc = "커서 근처 테스트 디버그",
		},
		{
			"<leader>Ts",
			function()
				require("neotest").summary.toggle()
			end,
			desc = "테스트 요약 창",
		},
		{
			"<leader>To",
			function()
				require("neotest").output.open({ enter = true, auto_close = true })
			end,
			desc = "테스트 출력 보기",
		},
	},
}
