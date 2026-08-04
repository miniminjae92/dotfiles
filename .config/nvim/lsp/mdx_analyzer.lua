-- mdx 안의 JSX를 타입 검사까지 시킨다(끄면 컴포넌트 오타를 못 잡는다).
return {
	filetypes = { "mdx" },
	init_options = {
		typescript = { enabled = true },
	},
}
