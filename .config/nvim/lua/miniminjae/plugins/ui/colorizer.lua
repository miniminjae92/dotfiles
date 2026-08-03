-- #hex·tailwind 클래스 옆에 실제 색을 보여준다. 색 코드를 머릿속에서 렌더링하지 않아도 된다.
return {
	"brenoprata10/nvim-highlight-colors",
	event = "VeryLazy",
	config = function()
		local colorizer = require("nvim-highlight-colors")
		local virtual = true

		local function apply()
			colorizer.setup({
				render = virtual and "virtual" or "background",
				enable_tailwind = true,
				virtual_symbol = "■",
			})
		end

		apply()

		-- 스티커(옆에 점) ↔ 형광펜(글자 배경) 전환
		vim.keymap.set("n", "<leader>tc", function()
			virtual = not virtual
			apply()
			colorizer.turnOff()
			colorizer.turnOn()
			vim.notify("색 표시: " .. (virtual and "스티커" or "형광펜"))
		end, { desc = "색 표시 방식 토글" })
	end,
}
