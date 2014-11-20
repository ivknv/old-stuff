" ==================================================
" Author: Ivan Konovalov
" Version: 1.6.2 2014.11.20 22:48 +0600
"
" Warning: I never tested this vimrc under Windows!
" ==================================================

" Backspace to delete text
set backspace=2

" Tabstop
set ts=4

" Shift width
set sw=4

" Disable tab to spaces
set noet

set nosmarttab

" Show current command
set showcmd

" Enable line break
set linebreak
set dy=lastline
set iminsert=0

set term=xterm-256color

" Set encodings
set encoding=utf8
set termencoding=utf8
set fileencoding=utf8
set fileencodings=utf8,cp1251,koi8-r,cp866

" Show line numbers
set number

" Enable mouse
set mouse=a

set fileformat=unix

" Enable wild menu
set wildmenu

" Enable status line
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

" Turn auto indent off
set noai

" Turn smart indent off
set nosi

" Reset Ctrl-S key
silent !stty stop undef

" Enable scrolling with mouse wheel
map <ScrollWheelUp> <C-Y>
imap <ScrollWheelUp> <C-O><C-Y>
xmap <ScrollWheelUp> <C-Y><C-Y>
map <ScrollWheelDown> <C-E>
imap <ScrollWheelDown> <C-O><C-E>
xmap <ScrollWheelDown> <C-E>

" Ctrl-S to save file
noremap <silent> <C-S> :update<CR>
vnoremap <silent> <C-S> <C-C>:update<CR>
inoremap <silent> <C-S> <C-O>:update<CR>

set wcm=<Tab>

menu Exec.Python :!python %<CR>
menu Exec.Python3 :!python3 %<CR>
menu Exec.VimScript :so %<CR>
menu Exec.REAPACHE :!sudo service apache2 reload<CR>

menu Run.IPython :!ipython<CR>
menu Run.IPython3 :!ipython3<CR>
menu Run.Python :!python<CR>
menu Run.Python3 :!python3<CR>
menu Run.MC :!mc<CR>
menu Run.Bash :!bash<CR>
menu Run.SH :!sh<CR>

menu Exit.Exit :q!<CR>
menu Exit.ExitAll :qall!<CR>
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

" F12 to exit
map <F12> :emenu Exit.<Tab>
imap <F12> <Esc>:emenu Exit.<Tab>

map <F8>f :emenu File.<Tab>

map <F8>e :emenu Encoding.<Tab>

map <F3> :emenu Run.<Tab>
imap <F3> <Esc>:emenu Run.<Tab>

" Escape < and >
map <F8>1 :s/</\&lt;/g<CR>:s/>/\&gt;/g<CR>
imap <F8>1 <C-O>:s/</\&lt;/g<CR>:s/>/\&gt;/g<CR>

" Replace &lt; and &gt; by < and >
map <F8>2 <C-O>:s/&lt;/</g<CR>:s/&gt;/>/g<CR>
imap <F8>2 <C-O>:s/&lt;/</g<CR>:s/&gt;/>/g<CR>

" Comment current line
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

" lisphelper.vim
"map <F8>l :call lisphelper#check_brackets()<CR>
"imap <F8>l <Esc><F8>l

nmap <Tab> :tabnew 

imap <F9> <Esc>:emenu Exec.<Tab>
map <F9> :emenu Exec.<Tab>

" Some key mappings from regular editors
map <F8><C-O> :tabnew! .<CR>
imap <F8><C-O> <C-O>:tabnew! .<CR>

" Select all
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

" Backspace in normal mode
map <Backspace> d<Left>

" Quickly change tab. Works in gVim only
imap <A-Left> <C-O>:tabprevious<CR>
imap <A-Right> <C-O>:tabnext<CR>
map <A-Left> <C-O>:tabprevious<CR>
map <A-Right> <C-O>:tabnext<CR>

" Undo
map <F5> u
imap <F5> <C-O>u

" Redo
map <F6> <C-R>
imap <F6> <C-O><C-R>

filetype plugin off

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

" Copy/Cut paste
xmap <C-C> "+y
xmap <C-X> "+c
imap <C-V> <C-R>+
nmap <C-V> "+p
xmap <C-V> "+p

" Awesome colorscheme
" set background=dark
" colorscheme hybrid
" set t_Co=256

" filetype plugin indent on
hi StatusLine ctermbg=None ctermfg=white

" Some shortcuts
au FileType html,htmldjango iabbr <buffer> linkhref <link rel="stylesheet" type="text/css" href="" /><Left><Left><Left><Left>
au FileType html,htmldjango iabbr <buffer> ahref <a href=""></a><Left><Left><Left><Left><Left><Left>
au FileType html,htmldjango iabbr <buffer> divclass <div class=""></div><Left><Left><Left><Left><Left><Left><Left><Left>
au FileType html,htmldjango iabbr <buffer> divid <div id=""></div><Left><Left><Left><Left><Left><Left><Left><Left>
au FileType html,htmldjango iabbr <buffer> spanclass <span class=""></span><Left><Left><Left><Left><Left><Left><Left><Left><Left>
au FileType html,htmldjango iabbr <buffer> spanid <span id=""></span><Left><Left><Left><Left><Left><Left><Left><Left><Left>
au FileType html,htmldjango iabbr <buffer> scriptsrc <script type="text/javascript" src=""></script><Left><Left><Left><Left><Left><Left><Left><Left><Left><Left><Left>
au FileType html,htmldjango iabbr <buffer> scriptt <script type="text/javascript"></script><Left><Left><Left><Left><Left><Left><Left><Left><Left>
au FileType html,htmldjango iabbr <buffer> <!D <!DOCTYPE><Left>
au FileType html,htmldjango iabbr <buffer> {% {% %}<Left><Left><Left>
au FileType html,htmldjango iabbr <buffer> {{ {{ }}<left><Left><Left>

au FileType python iabbr <buffer> def def():<Left><Left><Left>
au FileType python iabbr <buffer> class class:<Left>
au FileType python iabbr <buffer> if if:<Left>
au FileType python iabbr <buffer> elif elif:<Left>
au FileType python iabbr <buffer> except except:<Left>
au FileType python,java iabbr <buffer> im import
au FileType c,cpp iabbr <buffer> #d #define
au FileType c,cpp iabbr <buffer> #i #include

au FileType clojure,lisp setlocal ts=2

" Indentation fix for Python
" autocmd! BufNewFile,BufRead *.py setlocal ts=4 sw=4 noet

" Autocomplete with Tab
function! Tab_Or_Complete()
  if col('.')>1 && strpart( getline('.'), col('.')-2, 3 ) =~ '^\w'
	return "\<C-N>"
  else
	return "\<Tab>"
  endif
endfunction

inoremap <Tab> <C-R>=Tab_Or_Complete()<CR>

" File templates
au BufNewFile * silent! execute '0r ~/.vim/templates/default.%:e | normal GkJgg'

" Some functions
function! SpacesToTabs(num)
	let num_spaces = repeat(" ", a:num)
	execute "%s/" . num_spaces . "/\t/g"
endfunction

function! TabsToSpaces(num)
	let num_spaces = repeat(" ", a:num)
	execute "%s/\t/" . num_spaces ."/g"
endfunction

" Quickly replace spaces <--> tabs
command TabsToSpaces call TabsToSpaces(&ts)
command SpacesToTabs call SpacesToTabs(&ts)

set nocompatible
let conceal=1

let fortran_free_source=1
let fortran_have_tabs=1

syntax on
syntax enable

au FileType python set dictionary+=~/.vim/wordlists/python_wordlist.txt
au FileType javascript set dictionary+=~/.vim/wordlists/javascript_wordlist.txt
au FileType html,htmldjango set dictionary+=~/.vim/wordlists/html_wordlist.txt
au FileType css,sass set dictionary+=~/.vim/wordlists/css_wordlist.txt
set complete-=k complete+=k
