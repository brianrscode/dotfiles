-- bootstrap lazy.nvim, LazyVim and your plugins
require("config.lazy")
require("config.keymaps")

vim.wo.number = false

vim.api.nvim_exec(
  [[
  augroup trim_whitespace
    autocmd!
    autocmd BufWritePre * :%s/\s\+$//e
  augroup END
]],
  false
)
