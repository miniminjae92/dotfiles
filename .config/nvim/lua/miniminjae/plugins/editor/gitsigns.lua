-- 변경분을 줄 단위(헝크)로 보고 스테이징한다. 커밋 단위를 쪼개는 작업이 여기서 끝난다.
return {
	"lewis6991/gitsigns.nvim",
	event = { "BufReadPre", "BufNewFile" },
	opts = {
		on_attach = function(bufnr)
			local gs = require("gitsigns")

			local function map(mode, l, r, desc)
				vim.keymap.set(mode, l, r, { buffer = bufnr, desc = desc })
			end

			map("n", "]h", function()
				gs.nav_hunk("next")
			end, "다음 헝크")
			map("n", "[h", function()
				gs.nav_hunk("prev")
			end, "이전 헝크")

			map("n", "<leader>hs", gs.stage_hunk, "헝크 스테이징")
			map("n", "<leader>hr", gs.reset_hunk, "헝크 되돌리기")
			map("v", "<leader>hs", function()
				gs.stage_hunk({ vim.fn.line("."), vim.fn.line("v") })
			end, "선택 영역 스테이징")
			map("v", "<leader>hr", function()
				gs.reset_hunk({ vim.fn.line("."), vim.fn.line("v") })
			end, "선택 영역 되돌리기")

			map("n", "<leader>hS", gs.stage_buffer, "파일 전체 스테이징")
			map("n", "<leader>hR", gs.reset_buffer, "파일 전체 되돌리기")
			map("n", "<leader>hu", gs.undo_stage_hunk, "스테이징 취소")
			map("n", "<leader>hp", gs.preview_hunk, "헝크 미리보기")

			map("n", "<leader>hb", function()
				gs.blame_line({ full = true })
			end, "이 줄 blame")
			map("n", "<leader>hB", gs.toggle_current_line_blame, "줄 blame 상시 표시")

			map("n", "<leader>hd", gs.diffthis, "이 파일 diff")
			map("n", "<leader>hD", function()
				gs.diffthis("~")
			end, "직전 커밋과 diff")

			map({ "o", "x" }, "ih", ":<C-U>Gitsigns select_hunk<CR>", "헝크를 텍스트 오브젝트로")
		end,
	},
}
