-- 자동완성 엔진. nvim-cmp/LuaSnip 조합을 대체한다(매칭 품질·속도·설정 분량 때문에 고른 것).
-- 스니펫은 별도 엔진 없이 내장 vim.snippet을 쓰고, 스니펫 "파일"은 VSCode JSON 형식으로 둔다.
return {
	"saghen/blink.cmp",
	version = "1.*",
	dependencies = { "rafamadriz/friendly-snippets" },
	opts = {
		-- 손버릇 유지: 후보 이동은 <C-j>/<C-k>, 스니펫 점프는 <C-l>/<C-h>.
		keymap = {
			preset = "none",
			["<C-j>"] = { "select_next", "fallback" },
			["<C-k>"] = { "select_prev", "fallback" },
			["<C-u>"] = { "scroll_documentation_up", "fallback" },
			["<C-d>"] = { "scroll_documentation_down", "fallback" },
			["<C-Space>"] = { "show", "show_documentation", "hide_documentation" },
			["<C-e>"] = { "hide", "fallback" },
			["<CR>"] = { "accept", "fallback" },
			["<C-l>"] = { "snippet_forward", "fallback" },
			["<C-h>"] = { "snippet_backward", "fallback" },
		},

		appearance = { nerd_font_variant = "mono" },

		completion = {
			-- 아무것도 고르지 않은 상태로 뜬다. 엔터를 잘못 눌러 엉뚱한 후보가 박히는 걸 막는다.
			list = { selection = { preselect = false, auto_insert = false } },
			menu = { border = "rounded" },
			documentation = { auto_show = true, auto_show_delay_ms = 200, window = { border = "rounded" } },
		},

		signature = { enabled = true, window = { border = "rounded" } },

		snippets = {
			preset = "default",
			-- 날짜($CURRENT_*)와 경로($TM_DIRECTORY)는 blink이 알아서 채운다.
			-- 다만 "파일이 든 폴더 이름"에 해당하는 변수가 없다(TM_DIRECTORY는 전체 경로).
			-- vim.snippet은 변환(transform)을 지원하지 않으므로 $DIRNAME만 여기서 직접 채운다 — 글 slug가 이걸 쓴다.
			expand = function(snippet)
				local dirname = vim.fn.fnamemodify(vim.fn.expand("%:p:h"), ":t")
				vim.snippet.expand((snippet:gsub("%$DIRNAME", function()
					return dirname
				end)))
			end,
		},

		sources = {
			default = { "lazydev", "lsp", "path", "snippets", "buffer" },
			providers = {
				-- nvim 설정 lua에서만 붙는 타입 소스. LSP보다 앞세워야 vim.* 후보가 위로 온다.
				lazydev = { name = "LazyDev", module = "lazydev.integrations.blink", score_offset = 100 },
				snippets = {
					opts = {
						search_paths = { vim.fn.stdpath("config") .. "/snippets" },
					},
				},
			},
		},

		fuzzy = { implementation = "prefer_rust_with_warning" },
	},
	opts_extend = { "sources.default" },
}
