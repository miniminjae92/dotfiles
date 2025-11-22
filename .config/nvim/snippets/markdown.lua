local ls = require("luasnip")
local s = ls.snippet
local i = ls.insert_node
local f = ls.function_node
local fmt = require("luasnip.extras.fmt").fmt

return {
	s(
		{ trig = "fm", desc = "front-matter 기본 템플릿" },
		fmt(
			[[
---
title: "{}"
slug: {}
date: {}
description: "{}"
tags:
  - {}
---
]],
			{
				i(1, "제목"),

				f(function()
					return vim.fn.fnamemodify(vim.fn.expand("%:p:h"), ":t")
				end, {}),

				f(function()
					return os.date("%Y-%m-%d %H:%M")
				end, {}),

				i(2, "설명"),
				i(3, "태그"),
			}
		)
	),
}
