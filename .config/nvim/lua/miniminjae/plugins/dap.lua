return {
	"mfussenegger/nvim-dap",
	dependencies = {
		"rcarriga/nvim-dap-ui",
		"theHamsta/nvim-dap-virtual-text",
		"nvim-telescope/telescope-dap.nvim",
	},
	config = function()
		local dap = require("dap")
		local dapui = require("dapui")
		local dap_virtual_text = require("nvim-dap-virtual-text")

		-- C/C++ 디버깅 설정
		dap.adapters.cppdbg = {
			id = "cppdbg",
			type = "executable",
			command = "lldb-vscode",
			name = "lldb",
		}

		dap.configurations.cpp = {
			{
				name = "Launch",
				type = "cppdbg",
				request = "launch",
				program = function()
					return vim.fn.input("Path to executable: ", vim.fn.getcwd() .. "/", "file")
				end,
				cwd = "${workspaceFolder}",
				stopAtEntry = false,
				args = {},
				runInTerminal = false,
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
		dap_virtual_text.setup({
			display_callback = function(variable, _buf, _stackframe, _node, _options)
				return string.format("%s = %s", variable.name, variable.value)
			end,
		})

		-- 키맵 설정
		local keymap = vim.keymap

		keymap.set("n", "<leader>db", dap.toggle_breakpoint, { desc = "Toggle Breakpoint" })
		keymap.set("n", "<leader>dc", dap.continue, { desc = "Continue" })
		keymap.set("n", "<leader>di", dap.step_into, { desc = "Step Into" })
		keymap.set("n", "<leader>do", dap.step_over, { desc = "Step Over" })
		keymap.set("n", "<leader>dr", dap.repl.toggle, { desc = "Toggle REPL" })
		keymap.set("n", "<leader>dl", dap.run_last, { desc = "Run Last" })
		keymap.set("n", "<leader>du", dapui.toggle, { desc = "Toggle UI" })
		keymap.set("n", "<leader>dx", dap.terminate, { desc = "Terminate" })
		keymap.set("n", "<leader>dC", dap.clear_breakpoints, { desc = "Clear Breakpoints" })
	end,
} 