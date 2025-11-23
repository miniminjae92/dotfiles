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
	s(
		{ trig = "dimg", desc = "이미지 중앙 정렬 Div" },
		fmt(
			[[
<div className="mx-auto max-w-sm">
  ![{}]({})
</div>
]],
			{
				i(2, ""),
				i(1, ""),
			}
		)
	),
	s(
		{ trig = "dvideo", desc = "MP4를 GIF처럼 자동재생 (Video 태그)" },
		fmt(
			[[
<div className="mx-auto max-w-sm">
  <video src="{}" autoPlay loop muted playsInline className="w-full rounded-lg"></video>
</div>
]],
			{
				i(1, "비디오파일경로.mp4"),
			}
		)
	),
	s(
		{ trig = "sp", desc = "MDX Vertical Spacer" },
		fmt(
			[[
<Spacer y={{ {} }} />
]],
			{
				i(1, "4"),
			}
		)
	),
}
