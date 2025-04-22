return {
  "kylechui/nvim-surround",
  event = { "BufReadPre", "BufNewFile" },
  version = "*", -- Use for stability; omit to use `main` branch for the latest features
  config = true,
}
-- ys: "yank" + "surround" ex) ysiw"
-- cs: "change" + "surround" ex) cs"'
-- ds: "delete" + "surround" ex) ds"
