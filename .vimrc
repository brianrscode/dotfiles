syntax on
set autoindent
set encoding=UTF-8
set number nornu
set guifont="Mononoki Nerd Font":16
set splitbelow splitright

" Elimina todos los espacios al final de una línea
autocmd BufWritePre * :%s/\s\+$//e


" colorscheme atom-dark-256
let g:airline_theme='one'
colorscheme one
set background=dark " for the dark version


" Mapeo de la tecla Esc -> en vez de usar la tecla <Esc> se usa doble jota(j)
imap jj <Esc>

