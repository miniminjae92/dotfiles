return {
	{
		"brenoprata10/nvim-highlight-colors",
		event = "VeryLazy",
		config = function()
			local colorizer = require("nvim-highlight-colors")

			local is_virtual = true

			colorizer.setup({
				render = "virtual",
				enable_tailwind = true,
				virtual_symbol = "■",
			})

			local function toggle_render_mode()
				if is_virtual then
					colorizer.setup({
						render = "background",
						enable_tailwind = true,
					})
					is_virtual = false
					print("🎨 Color Mode: Background (형광펜)")
				else
					colorizer.setup({
						render = "virtual",
						enable_tailwind = true,
						virtual_symbol = "■",
					})
					is_virtual = true
					print("🎨 Color Mode: Virtual (스티커)")
				end
				colorizer.turnOff()
				colorizer.turnOn()
			end

			vim.keymap.set("n", "<leader>tc", toggle_render_mode, { desc = "Toggle Color Render Mode" })
		end,
	},
}
