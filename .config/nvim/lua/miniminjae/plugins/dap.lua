-- lua/miniminjae/plugins/dap.lua
return {
	"mfussenegger/nvim-dap",
	dependencies = {
		"nvim-neotest/nvim-nio",
		"rcarriga/nvim-dap-ui",
		"theHamsta/nvim-dap-virtual-text",
		"nvim-telescope/telescope-dap.nvim",
	},
	config = function()
		local dap = require("dap")
		local dapui = require("dapui")
		local dap_virtual_text = require("nvim-dap-virtual-text")

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

		-- 가상 텍스트 (변수 옆에 값 보여주기)
		dap_virtual_text.setup()

		-- 디버깅 시작/종료 시 UI 자동으로 열고 닫기
		dap.listeners.after.event_initialized["dapui_config"] = function()
			dapui.open()
		end
		dap.listeners.before.event_terminated["dapui_config"] = function()
			dapui.close()
		end
		dap.listeners.before.event_exited["dapui_config"] = function()
			dapui.close()
		end

		local keymap = vim.keymap

		keymap.set("n", "<leader>db", dap.toggle_breakpoint, { desc = "Debug: Toggle Breakpoint" })
		keymap.set("n", "<leader>dc", dap.continue, { desc = "Debug: Continue" })
		keymap.set("n", "<leader>di", dap.step_into, { desc = "Debug: Step Into" })
		keymap.set("n", "<leader>do", dap.step_over, { desc = "Debug: Step Over" })
		keymap.set("n", "<leader>dO", dap.step_out, { desc = "Debug: Step Out" })
		keymap.set("n", "<leader>dr", dap.repl.toggle, { desc = "Debug: Toggle REPL" })
		keymap.set("n", "<leader>dl", dap.run_last, { desc = "Debug: Run Last" })
		keymap.set("n", "<leader>du", dapui.toggle, { desc = "Debug: Toggle UI" })
		keymap.set("n", "<leader>dx", dap.terminate, { desc = "Debug: Terminate" })

		-- [IntelliJ 스타일] 펑션키 조합
		-- F9: Resume Program (다음 브레이크포인트까지 실행)
		keymap.set("n", "<F9>", dap.continue, { desc = "Debug: Resume (IntelliJ F9)" })

		-- F8: Step Over (함수 건너뛰고 다음 줄)
		keymap.set("n", "<F8>", dap.step_over, { desc = "Debug: Step Over (IntelliJ F8)" })

		-- F7: Step Into (함수 안으로)
		keymap.set("n", "<F7>", dap.step_into, { desc = "Debug: Step Into (IntelliJ F7)" })

		-- Shift + F8: Step Out (함수 밖으로)
		keymap.set("n", "<S-F8>", dap.step_out, { desc = "Debug: Step Out (IntelliJ Shift+F8)" })

		-- Ctrl + F8: Breakpoint Toggle (맥 OS 단축키와 겹칠 수 있음 주의)
		keymap.set("n", "<C-F8>", dap.toggle_breakpoint, { desc = "Debug: Toggle Breakpoint" })

		-- 평가(Evaluate) 관련
		keymap.set("n", "<leader>de", function()
			dapui.eval(nil, { enter = true })
		end, { desc = "Debug: Evaluate (Cursor)" })
	end,
}
