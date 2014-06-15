" ==================================================
" Author: Ivan Konovalov
" Version: 1.5.2 2014.06.14 21:46 +0600
" 
" Warning: I never tested this vimrc under Windows!
" ==================================================

set backspace=2

" Tabstop
set ts=4

" Shift width
set sw=4

" Disable tab to spaces
set noet
set smarttab
set showcmd
set linebreak
set dy=lastline
set iminsert=0
set encoding=utf8
set term=xterm-256color
set termencoding=utf8
set fileencoding=utf8
set fileencodings=utf8,cp1251,koi8-r,cp866
set number
set mouse=a
set fileformat=unix
set wildmenu
set laststatus=2

" Automaticaly read file when it's modified
set autoread

" Ignore case when searching
set ignorecase

" Enable 'smart case' when searching
set smartcase

" Highlight search results
set hlsearch

" Scroll to search results when writting search pattern
set incsearch

" Don't redraw window while executing macros
set lazyredraw

" Turn regular expression 'magic' on
set magic

" Show matching brackets
set showmatch

" Turn annoying sounds off
set noerrorbells
set novisualbell

" Turn auto indent on
set ai

" Turn smart indent on
set si

" Reset <C-S> key
silent !stty stop undef

" Enable mouse scrolling
map <ScrollWheelUp> <C-Y>
imap <ScrollWheelUp> <C-O><C-Y>
xmap <ScrollWheelUp> <C-Y><C-Y>
map <ScrollWheelDown> <C-E>
imap <ScrollWheelDown> <C-O><C-E>
xmap <ScrollWheelDown> <C-E>

" <C-S> to save file
noremap <silent> <C-S> :update<CR>
vnoremap <silent> <C-S> <C-C>:update<CR>
inoremap <silent> <C-S> <C-O>:update<CR>

set wcm=<Tab>

menu Exec.Python :!python %<CR>
menu Exec.Python3 :!python3 %<CR>
menu Exec.VimScript :so %<CR>
menu Exec.REAPACHE :!sudo service apache2 reload<CR>

menu Run.IPython :!ipython<CR>
menu Run.Python :!python<CR>
menu Run.Python3 :!python3<CR>
menu Run.MC :!mc<CR>
menu Run.Bash :!bash<CR>
menu Run.SH :!sh<CR>

menu Exit.Exit :q!<CR>
menu Exit.Save&Exit :wq!<CR>
menu Exit.CloseTab :tabclose!<CR>

menu File.Save :w!<CR>
menu File.Remove :call delete(expand('%'))
menu File.Rename :!mv % 

menu Encoding.UTF-8 :e ++enc=utf8<CR>
menu Encoding.CP-1251 :e ++enc=cp1251<CR>
menu Encoding.KOI8-R :e ++enc=koi8-r<CR>
menu Encoding.CP-866 :e ++enc=cp866<CR>

map <Space> /

map , :emenu Exec.<Tab>

map <F12> :emenu Exit.<Tab>
imap <F12> <Esc>:emenu Exit.<Tab>

map fi :emenu File.<Tab>

map enc :emenu Encoding.<Tab>

map <F3> :emenu Run.<Tab>
imap <F3> <Esc>:emenu Run.<Tab>

map <F8>1 :s/</\&lt;/g<CR>:s/>/\&gt;/g<CR>
imap <F8>1 <C-O>:s/</\&lt;/g<CR>:s/>/\&gt;/g<CR>

map <F8>2 <C-O>:s/&lt;/</g<CR>:s/&gt;/>/g<CR>
imap <F8>2 <C-O>:s/&lt;/</g<CR>:s/&gt;/>/g<CR>

map <F8># <C-0>i#<Esc>
imap <F8># <C-O><C-0>#

map <F8>" <C-0>i"""<C-O>$"""<Esc>
imap <F8>" <C-O><C-0>"""<C-O>$"""

map <F8>// <C-0>i//<Esc>
imap <F8>// <C-O><C-0>//

map <F8>/* <C-0>i/*<C-O>$*/<Esc>
imap <F8>/* <C-O><C-0>/*<C-O>$*/

map <F8>; <C-0>i;<Esc>
imap <F8>; <C-O><C-0>;

map <F8>< <C-0>i<!--<C-O>$--><Esc>
imap <F8>< <C-O><C-0><!--<C-O>$-->

map <F8>- <C-0>i--<Esc>
imap <F8>- <C-O><C-0>--

nmap <Tab> :tabnew 

imap <F9> <Esc>:emenu Exec.<Tab>
map <F9> :emenu Exec.<Tab>

" Some key mappings from regular editors
map <F8><C-O> :tabnew! .<CR>
imap <F8><C-O> <C-O>:tabnew! .<CR>
imap <C-A> <Esc>ggvG$
map <C-A> ggvG$
imap <S-End> <C-O>v$
map <S-End> v$
imap <S-Home> <C-O>v0
map <S-Home> v0
imap <C-S-Home> <C-O>$v0
map <C-S-Home> $v0
imap <C-S-End> <C-O>0v$
map <C-S-End> 0v$
map <Backspace> d<Left>

map <F6> <C-R>
imap <F6> <C-O><C-R>

imap <A-Left> <C-O>:tabprevious<CR>
imap <A-Right> <C-O>:tabnext<CR>

map <C-U> u
imap <C-U> <C-O>u

map <F5> u
imap <F5> <C-O>u

filetype plugin on

" Text selection like in regular editors
nmap <S-Left> v<Left>
nmap <S-Right> v<Right>
nmap <S-Down> v<Down>
nmap <S-Up> v<Up>
imap <S-Left> <C-O>v<Left>
imap <S-Right> <C-O>v<Right>
imap <S-Down> <C-O>v<Down>
imap <S-Up> <C-O>v<Up>
xmap <S-Up> <Up>
xmap <S-Down> <Down>
xmap <S-Left> <Left>
xmap <S-Right> <Right>

xmap <C-C> "+y
xmap <C-X> "+c
imap <C-V> <C-R>+
nmap <C-V> "+p

set background=dark
colorscheme jellybeans
set t_Co=256
syntax on
filetype plugin indent on
hi StatusLine ctermbg=None ctermfg=white

iabbr scriptsrc <script type="text/javascript" src=""></script><Left><Left><Left><Left><Left><Left><Left><Left><Left><Left><Left>
iabbr linkhref <link rel="stylesheet" type="text/css" href="" /><Left><Left><Left><Left>
iabbr ahref <a href=""></a><Left><Left><Left><Left><Left><Left>
iabbr divclass <div class=""></div><Left><Left><Left><Left><Left><Left><Left><Left>
iabbr divid <div id=""></div><Left><Left><Left><Left><Left><Left><Left><Left>
iabbr spanclass <span class=""></span><Left><Left><Left><Left><Left><Left><Left><Left><Left>
iabbr scriptsrc <script type="text/javascript" src=""></script><Left><Left><Left><Left><Left><Left><Left><Left><Left><Left><Left>
iabbr scriptt <script type="text/javascript"><CR><CR></script><Left><Left><Left><Left><Left><Left><Left><Left><Left><Up>

iabbr def def():<Left><Left><Left>
iabbr im import
iabbr #d #define

autocmd FileType clojure :iabbr () ( )<Left><Left>
iabbr <!D <!DOCTYPE><Left>
iabbr {% {% %}<Left><Left><Left>
iabbr {{ {{ }}<left><Left><Left>
iabbr #i #include

autocmd! BufNewFile,BufRead *.py setlocal ts=4 sw=4 noet