set number
set clipboard=unnamed

set autoindent
set smartindent

set tabstop=4
set shiftwidth=4
set noexpandtab

inoremap " ""<left>
inoremap ' ''<left>
inoremap ( ()<left>
inoremap [ []<left>
inoremap { {}<left>
inoremap {<CR> {<CR>}<ESC>O
inoremap {;<CR> {<CR>};<ESC>O

" Syntax Highlighting
if has("syntax")
    syntax on
endif

set hlsearch " 검색어 하이라이팅
set incsearch " 점진적 검색 

"set laststatus=2 " 상태바 표시를 항상한다
"set statusline=\ %<%l:%v\ [%P]%=%a\ %h%m%r\ %F\

"커서를 마지막 수정 위치로 이동
au BufReadPost *
\ if line("'\"") > 0 && line("'\"") <= line("$") |
\   exe "norm g`\"" |
\ endif

" call plug#begin('~/.vim/plugged')
"
" call plug#end()
