-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua

--------------------------------------------------
--------------------------------------------------
----- Definición de funciones para shortcuts -----
--------------------------------------------------
--------------------------------------------------

local function map(mode, lhs, rhs, opts)
  local options = { noremap = true, silent = true }
  if opts then
    options = vim.tbl_extend("force", options, opts)
  end
  -- vim.api.nvim_set_keymap(mode, lhs, rhs, options)
  vim.keymap.set(mode, lhs, rhs, options)
end

----------------------
----------------------
-- Neovim shortcuts --
----------------------
----------------------

-- Disable arrow keys in mode Insert and Read
map("", "<up>", "<nop>")
map("", "<down>", "<nop>")
map("", "<left>", "<nop>")
map("", "<right>", "<nop>")

map("i", "<up>", "<nop>")
map("i", "<down>", "<nop>")
map("i", "<left>", "<nop>")
map("i", "<right>", "<nop>")

-- Map Esc to jj
-- Mapea "jj" en el modo de inserción para remplazarla por un escape <esc>
map("i", "jj", "<Esc>")

map("n", "<C-j>", "10<C-e>") -- Baja 10 líneas
map("n", "<C-k>", "10<C-y>") -- Sube 10 líneas

map("n", "<leader>w", "<cmd>:w<CR>") -- "Espacio + w" guarda el documento
map("n", "<leader>q", "<cmd>:q<CR>") -- "Espacio + q" cierra el documento

map("n", "<leader>i", "A;<ENTER>") -- "Espacio + i" Agrega un ; al final de la línea y da un salto
map("n", "<leader>o", "A{<ENTER>}<Esc>O") -- "Espacio + i" Agrega un { al final de la línea y da un salto
