local mapKey = require("utils.keyMapper").mapKey

return {
  {
    "akinsho/toggleterm.nvim",
    version = "*",
    config = function()
      require("toggleterm").setup({
        open_mapping = [[<c-\>]],
        direction = "float",
      })

      -- C-\ 키에 대해 현재 파일의 디렉토리로 이동 후 터미널 열기
      mapKey([[<C-\>]], function()
        -- 현재 파일 경로에서 디렉토리 추출
        local dir = vim.fn.expand("%:h")
        if dir ~= "" then
          vim.cmd("lcd " .. dir) -- 디렉토리 변경
        end
        -- ToggleTerm 열기
        vim.cmd("ToggleTerm")
      end)

      -- ToggleTerm 키 매핑
      mapKey([[<leader>tv]], "<Cmd>ToggleTerm direction=vertical<CR>")   -- 세로 모드
      mapKey([[<leader>th]], "<Cmd>ToggleTerm direction=horizontal<CR>") -- 가로 모드

      -- 터미널 종료 키 설정
      mapKey("<leader>q", [[<C-\><C-n>:q!<CR>]], "t")
      mapKey("<leader>q", "<Cmd>q!<CR>", "n")

      -- 터미널 모드에서 esc 키로 빠져나오기
      mapKey("<esc>", [[<C-\><C-n>]], "t")

      -- 창 이동 키 설정
      mapKey("<C-k>", [[<C-\><C-n><C-W>k]], "t")
    end
  }
}

