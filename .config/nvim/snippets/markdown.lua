local ls = require("luasnip")
local s = ls.snippet
local t = ls.text_node
local i = ls.insert_node
local fmt = require("luasnip.extras.fmt").fmt

local current_date = os.date("%Y-%m-%d %H:%M")

return {
	s(
		"fm",
		fmt(
			[[
---
title: {}
slug: {}
date: {}
description: {}
tags:
  - {}
---
]],
			{
				i(1, "제목을 입력하세요"),
				i(2, "slug-url"),
				t(current_date),
				i(3, "글의 간략한 요약입니다."),
				i(4, "nextjs"),
			}
		)
	),
}
