-- nvim 설정을 쓰는 언어라 `vim` 전역을 모르면 온통 경고가 뜬다. 라이브러리 경로는 lazydev가 채운다.
return {
	settings = {
		Lua = {
			diagnostics = { globals = { "vim" } },
			completion = { callSnippet = "Replace" },
		},
	},
}
