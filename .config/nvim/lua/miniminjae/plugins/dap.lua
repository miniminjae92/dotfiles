-- 디버깅의 언어 무관 부분: UI 배치·거터 표시·키맵. 어댑터(무엇을 붙일지)는 lang/이 꽂는다.
-- 그래서 이 파일만으로는 아무것도 디버깅하지 못한다 — 그게 의도다.
return {
	"mfussenegger/nvim-dap",
	dependencies = {
		"nvim-neotest/nvim-nio",
		"rcarriga/nvim-dap-ui",
		"theHamsta/nvim-dap-virtual-text",
	},
	config = function()
		local dap = require("dap")
		local dapui = require("dapui")

		dapui.setup({
			layouts = {
				{
					elements = {
						{ id = "scopes", size = 0.25 },
						{ id = "breakpoints", size = 0.25 },
						{ id = "stacks", size = 0.25 },
						{ id = "watches", size = 0.25 },
					},
					position = "left",
					size = 40,
				},
				{
					elements = {
						{ id = "repl", size = 0.5 },
						{ id = "console", size = 0.5 },
					},
					position = "bottom",
					size = 10,
				},
			},
		})

		-- 변수 값을 코드 옆에 바로 띄운다(값 보려고 watch 창을 오갈 필요를 줄인다)
		require("nvim-dap-virtual-text").setup({})

		-- 거터 표시. 중단점 종류를 모양으로 구분한다.
		local signs = {
			DapBreakpoint = { text = "●", texthl = "DiagnosticSignError" },
			DapBreakpointCondition = { text = "◆", texthl = "DiagnosticSignWarn" },
			DapLogPoint = { text = "○", texthl = "DiagnosticSignInfo" },
			DapBreakpointRejected = { text = "◉", texthl = "DiagnosticSignHint" },
			DapStopped = { text = "▶", texthl = "DiagnosticSignWarn", linehl = "Visual" },
		}
		for name, opts in pairs(signs) do
			vim.fn.sign_define(name, opts)
		end

		-- 세션이 시작되면 UI를 열고, 끝나면 닫는다
		dap.listeners.after.event_initialized["dapui"] = function()
			dapui.open()
		end
		dap.listeners.before.event_terminated["dapui"] = function()
			dapui.close()
		end
		dap.listeners.before.event_exited["dapui"] = function()
			dapui.close()
		end

		local map = function(lhs, rhs, desc)
			vim.keymap.set("n", lhs, rhs, { desc = desc })
		end

		map("<leader>db", dap.toggle_breakpoint, "중단점 토글")
		map("<leader>dc", dap.continue, "계속 실행 / 시작")
		map("<leader>di", dap.step_into, "함수 안으로")
		map("<leader>do", dap.step_over, "다음 줄로")
		map("<leader>dO", dap.step_out, "함수 밖으로")
		map("<leader>dr", dap.repl.toggle, "REPL 토글")
		map("<leader>dl", dap.run_last, "직전 설정으로 다시 실행")
		map("<leader>du", dapui.toggle, "디버그 UI 토글")
		map("<leader>dx", dap.terminate, "세션 종료")
		map("<leader>de", function()
			dapui.eval(nil, { enter = true })
		end, "커서 아래 값 평가")

		-- IntelliJ와 같은 펑션키 배치. 손이 기억하는 쪽을 그대로 둔다.
		map("<F9>", dap.continue, "계속 실행 (IntelliJ F9)")
		map("<F8>", dap.step_over, "다음 줄로 (IntelliJ F8)")
		map("<F7>", dap.step_into, "함수 안으로 (IntelliJ F7)")
		map("<S-F8>", dap.step_out, "함수 밖으로 (IntelliJ Shift+F8)")
		map("<C-F8>", dap.toggle_breakpoint, "중단점 토글 (IntelliJ Ctrl+F8)")
	end,
}
