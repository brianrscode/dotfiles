-- bootstrap lazy.nvim, LazyVim and your plugins
require("config.lazy")
require("config.keymaps")

-- vim.cmd("set langmenu=es_Es.UTF8")

-- :set number nornu
vim.wo.number = true
vim.wo.relativenumber = false

-- Elimina los espacios en blanco que haya al final de cada línea
vim.api.nvim_exec(
  [[
  augroup trim_whitespace
    autocmd!
    autocmd BufWritePre * :%s/\s\+$//e
  augroup END
]],
  false
)
