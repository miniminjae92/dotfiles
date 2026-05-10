return {
	"mistweaverco/kulala.nvim",
	ft = { "http", "rest" },
	config = function()
		require("kulala").setup({
			default_view = "body",
		})

		local keymap = vim.keymap

		keymap.set("n", "<leader>hr", function()
			require("kulala").run()
		end, { desc = "Run HTTP Request (kulala)" })

		keymap.set("n", "<leader>ht", function()
			require("kulala").toggle_view()
		end, { desc = "Toggle Headers/Body" })

		keymap.set("n", "[h", function()
			require("kulala").jump_prev()
		end, { desc = "Previous HTTP Request" })
		keymap.set("n", "]h", function()
			require("kulala").jump_next()
		end, { desc = "Next HTTP Request" })

		keymap.set("n", "<leader>hs", function()
			require("kulala").scratchpad()
		end, { desc = "Open Scratchpad" })
	end,
}
