return {
	"L3MON4D3/LuaSnip",
	config = function(_, opts)
		require("luasnip").setup(opts)

		require("luasnip.loaders.from_lua").load({
			paths = vim.fn.stdpath("config") .. "/snippets",
		})

		require("luasnip").filetype_extend("mdx", { "markdown" })

		require("luasnip").filetype_extend("mdx", { "html" })
	end,
}
