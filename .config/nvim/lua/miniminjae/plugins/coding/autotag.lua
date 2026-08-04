-- <div>을 닫으면 </div>이 따라오고, 여는 태그 이름을 고치면 닫는 태그도 같이 바뀐다.
-- treesitter main 브랜치에서는 treesitter 설정에 얹히지 않고 이 플러그인이 직접 setup한다.
return {
	"windwp/nvim-ts-autotag",
	ft = {
		"html",
		"javascript",
		"javascriptreact",
		"typescript",
		"typescriptreact",
		"svelte",
		"markdown",
		"mdx",
	},
	opts = {},
}
