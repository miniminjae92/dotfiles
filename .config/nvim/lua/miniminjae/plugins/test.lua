-- 테스트 실행의 언어 무관 부분. 어댑터는 lang/<언어>.lua가 opts.adapters에 꽂는다.
-- 키가 문자열이면 모듈 이름으로 보고 require해서 붙인다(설정 테이블이 있으면 넘겨준다).
return {
	"nvim-neotest/neotest",
	dependencies = {
		"nvim-neotest/nvim-nio",
		"nvim-lua/plenary.nvim",
		"nvim-treesitter/nvim-treesitter",
	},
	opts = {
		adapters = {},
		output = { open_on_run = false },
		output_panel = {
			open = function()
				return require("miniminjae.test_tool_window").create_window()
			end,
		},
	},
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
		require("miniminjae.test_tool_window").setup()
	end,
	keys = {
		{ "<leader>1", "<leader>Tx", remap = true, desc = "테스트 / 디버그 중지 (IdeaVim)" },
		{ "<leader>2", "<leader>Tf", remap = true, desc = "현재 파일 테스트 (IdeaVim RunClass)" },
		{ "<leader>3", "<leader>TD", remap = true, desc = "현재 파일 디버그 (IdeaVim DebugClass)" },
		{ "<leader>4", "<leader>Tt", remap = true, desc = "커서 근처 테스트 (IdeaVim Run)" },
		{ "<leader>5", "<leader>Td", remap = true, desc = "커서 근처 테스트 디버그 (IdeaVim Debug)" },
		{
			"<leader>Tx",
			function()
				local dap = require("dap")
				if dap.session() then
					dap.terminate()
				else
					require("neotest").run.stop()
				end
			end,
			desc = "테스트 / 디버그 중지",
		},
		{
			"<leader>Tf",
			function()
				require("miniminjae.test_tool_window").run(vim.fn.expand("%"))
			end,
			desc = "현재 파일 테스트",
		},
		{
			"<leader>TD",
			function()
				require("neotest").run.run({ vim.fn.expand("%"), strategy = "dap" })
			end,
			desc = "현재 파일 테스트 디버그",
		},
		{
			"<leader>Tt",
			function()
				require("miniminjae.test_tool_window").run()
			end,
			desc = "커서 근처 테스트",
		},
		{
			"<leader>Td",
			function()
				require("neotest").run.run({ strategy = "dap" })
			end,
			desc = "커서 근처 테스트 디버그",
		},
		{
			"<leader>Ta",
			function()
				require("miniminjae.test_tool_window").run(vim.uv.cwd())
			end,
			desc = "프로젝트 전체 테스트",
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
				require("miniminjae.test_tool_window").toggle()
			end,
			desc = "테스트 도구 창 열기 / 숨기기",
		},
		{
			"<leader>Ty",
			function()
				require("miniminjae.test_tool_window").copy_all()
			end,
			desc = "테스트 결과 복사",
		},
	},
}
