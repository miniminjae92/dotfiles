-- plugins/dap.lua
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

		-- codelldb 설정
		dap.adapters.codelldb = {
			type = "server",
			port = "${port}",
			executable = {
				command = vim.fn.stdpath("data") .. "/mason/bin/codelldb",
				args = { "--port", "${port}" },
			},
		}

		dap.configurations.cpp = {
			{
				name = "Launch file",
				type = "codelldb",
				request = "launch",
				program = function()
					return vim.fn.input("Path to executable: ", vim.fn.getcwd() .. "/", "file")
				end,
				cwd = "${workspaceFolder}",
				stopOnEntry = false,
				args = {},
			},
		}

		-- C 설정도 C++와 동일하게 사용
		dap.configurations.c = dap.configurations.cpp

		-- DAP UI 설정
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

		-- 가상 텍스트 설정
		dap_virtual_text.setup()

		-- 자동으로 UI 열기/닫기
		dap.listeners.after.event_initialized["dapui_config"] = function()
			dapui.open()
		end
		dap.listeners.before.event_terminated["dapui_config"] = function()
			dapui.close()
		end
		dap.listeners.before.event_exited["dapui_config"] = function()
			dapui.close()
		end

		-- 키맵 설정
		local keymap = vim.keymap

		-- 기본 디버깅 키맵
		keymap.set("n", "<leader>db", dap.toggle_breakpoint, { desc = "Toggle Breakpoint" })
		keymap.set("n", "<leader>dc", dap.continue, { desc = "Continue" })
		keymap.set("n", "<leader>di", dap.step_into, { desc = "Step Into" })
		keymap.set("n", "<leader>do", dap.step_over, { desc = "Step Over" })
		keymap.set("n", "<leader>dr", dap.repl.toggle, { desc = "Toggle REPL" })
		keymap.set("n", "<leader>dl", dap.run_last, { desc = "Run Last" })
		keymap.set("n", "<leader>du", dapui.toggle, { desc = "Toggle UI" })
		keymap.set("n", "<leader>dx", dap.terminate, { desc = "Terminate" })
		keymap.set("n", "<leader>dC", function()
			dap.clear_breakpoints()
			require("notify")("Breakpoints cleared", "warn")
		end, { desc = "Clear Breakpoints" })

		-- CLion 스타일 추가 키맵
		keymap.set("n", "<F5>", dap.continue, { desc = "Debug: Start/Continue" })
		keymap.set("n", "<F10>", dap.step_over, { desc = "Debug: Step Over" })
		keymap.set("n", "<F11>", dap.step_into, { desc = "Debug: Step Into" })
		keymap.set("n", "<S-F11>", dap.step_out, { desc = "Debug: Step Out" })
		keymap.set("n", "<F9>", dap.toggle_breakpoint, { desc = "Debug: Toggle Breakpoint" })
		keymap.set("n", "<leader>dB", function()
			dap.set_breakpoint(vim.fn.input("Breakpoint condition: "))
		end, { desc = "Debug: Set Conditional Breakpoint" })
		keymap.set("n", "<leader>dp", function()
			dap.set_breakpoint(nil, nil, vim.fn.input("Log point message: "))
		end, { desc = "Debug: Set Log Point" })
		keymap.set("n", "<leader>dE", function()
			dapui.eval(vim.fn.input("Expression: "))
		end, { desc = "Debug: Evaluate Expression" })
		keymap.set("n", "<leader>dS", function()
			dapui.float_element("scopes", { enter = true })
		end, { desc = "Debug: Show Scopes" })
		keymap.set("n", "<leader>dh", function()
			dapui.float_element("hover", { enter = true })
		end, { desc = "Debug: Hover Variables" })
		keymap.set("v", "<leader>dh", function()
			dapui.eval()
		end, { desc = "Debug: Evaluate Selection" })
	end,
}
