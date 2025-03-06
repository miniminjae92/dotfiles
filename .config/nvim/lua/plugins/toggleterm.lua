local mapKey = require("utils.keyMapper").mapKey

return {
  {
    "akinsho/toggleterm.nvim",
    version = "*",
    config = function()
      require("toggleterm").setup({
        open_mapping = [[<c-\>]],
        direction = "horizontal",
      })

      mapKey([[<leader>\]], "<Cmd>ToggleTerm direction=float<CR>")
      mapKey([[<leader>\]], "<Cmd>ToggleTerm<CR>", "t")
      mapKey("<leader>q", [[<C-\><C-n>:q!<CR>]], "t")
      mapKey("<esc>", [[<C-\><C-n>]], "t")
      mapKey("<C-k>", [[<C-\><C-n><C-W>k]], "t")
    end
  },
}
