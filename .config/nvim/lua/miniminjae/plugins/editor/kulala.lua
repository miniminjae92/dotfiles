-- .http 파일로 API를 때려본다. Postman 대신 요청을 코드처럼 저장소에 두려는 것.
-- 키맵은 버퍼 지역으로 건다 — 전역으로 걸면 gitsigns의 [h/]h와 부딪힌다.
return {
	"mistweaverco/kulala.nvim",
	ft = { "http", "rest" },
	opts = { default_view = "body" },
	config = function(_, opts)
		require("kulala").setup(opts)

		vim.api.nvim_create_autocmd("FileType", {
			group = vim.api.nvim_create_augroup("miniminjae_kulala", { clear = true }),
			pattern = { "http", "rest" },
			callback = function(ev)
				local function map(lhs, fn, desc)
					vim.keymap.set("n", lhs, fn, { buffer = ev.buf, desc = desc })
				end
				map("<leader>kr", function()
					require("kulala").run()
				end, "요청 실행")
				map("<leader>kt", function()
					require("kulala").toggle_view()
				end, "헤더/본문 전환")
				map("<leader>ks", function()
					require("kulala").scratchpad()
				end, "스크래치패드")
				map("]r", function()
					require("kulala").jump_next()
				end, "다음 요청")
				map("[r", function()
					require("kulala").jump_prev()
				end, "이전 요청")
			end,
		})
	end,
}
