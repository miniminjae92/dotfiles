filetype plugin indent on
syntax on

let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_browse_split = 4
let g:netrw_winsize = 20
let mapleader = " "

set number
set clipboard=unnamed
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent
set ignorecase
set smartcase
set incsearch
set hlsearch
set splitright
set splitbelow
set scrolloff=5

nnoremap <leader>sc :source ~/.vimrc<CR>
nnoremap <leader>ee :Lexplore<CR>
nnoremap <leader>sh :sp<CR>
nnoremap <leader>sv :vsp<CR>
nnoremap <leader>hh :nohlsearch<CR>
nnoremap <leader>nn :set number!<CR>

augroup netrw_start
    autocmd!
    autocmd VimEnter * if argc() == 1 && isdirectory(argv(0)) | enew | execute 'Lexplore ' . fnameescape(argv(0)) | endif
augroup END

augroup netrw_keys
    autocmd!
    autocmd FileType netrw nnoremap <buffer> <nowait> q :close<CR>
augroup END

augroup restore_cursor
    autocmd!
    autocmd BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$") | execute "normal! g`\"" | endif
augroup END
