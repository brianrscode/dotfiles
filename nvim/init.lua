require("config.lazy")
require("config.keymaps")

-- :set number nornu
vim.wo.number = true
vim.wo.relativenumber = true --false

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
