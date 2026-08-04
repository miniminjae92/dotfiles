-- 타이핑 자체를 줄이는 작은 도구들. 하나씩은 사소하지만 손에 붙으면 편집 속도를 바꾼다.
return {
	-- ys/cs/ds — 따옴표·괄호·태그를 감싸고 바꾸고 지운다
	{
		"kylechui/nvim-surround",
		event = { "BufReadPre", "BufNewFile" },
		version = "*",
		opts = {},
	},

	-- 여는 괄호를 치면 닫는 괄호를 붙인다 (nvim-autopairs 대체)
	{
		"echasnovski/mini.pairs",
		event = "InsertEnter",
		opts = {},
	},

	-- 내장 gc 주석이 jsx/svelte처럼 한 파일에 문법이 섞인 곳에서도 맞는 주석 기호를 고르게 한다
	{
		"folke/ts-comments.nvim",
		event = "VeryLazy",
		opts = {},
	},

	-- s{모션} — 레지스터 내용으로 갈아끼운다. 복사 → 여러 곳에 덮어쓰기가 한 동작이 된다
	{
		"gbprod/substitute.nvim",
		event = { "BufReadPre", "BufNewFile" },
		opts = {},
		keys = {
			{
				"s",
				function()
					require("substitute").operator()
				end,
				desc = "모션 범위를 레지스터로 치환",
			},
			{
				"ss",
				function()
					require("substitute").line()
				end,
				desc = "한 줄 치환",
			},
			{
				"S",
				function()
					require("substitute").eol()
				end,
				desc = "줄 끝까지 치환",
			},
			{
				"s",
				function()
					require("substitute").visual()
				end,
				mode = "x",
				desc = "선택 영역 치환",
			},
		},
	},

	-- `<leader>;`가 부르는 문장 종결 판단기(세미콜론이냐 콤마냐)
	{
		"lfilho/cosco.vim",
		event = { "BufReadPre", "BufNewFile" },
		dependencies = { "tpope/vim-repeat" },
	},
}
