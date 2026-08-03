-- svelte 서버는 컴포넌트 밖 .js/.ts가 바뀐 걸 스스로 모른다. 저장 시점에 직접 알려줘야 타입이 갱신된다.
return {
	on_attach = function(client)
		vim.api.nvim_create_autocmd("BufWritePost", {
			pattern = { "*.js", "*.ts" },
			callback = function(ctx)
				client:notify("$/onDidChangeTsOrJsFile", { uri = vim.uri_from_fname(ctx.match) })
			end,
		})
	end,
}
