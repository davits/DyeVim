" The MIT License (MIT)
"
" Copyright (c) 2016 Davit Samvelyan
"
" Permission is hereby granted, free of charge, to any person obtaining a copy
" of this software and associated documentation files (the "Software"), to deal
" in the Software without restriction, including without limitation the rights
" to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
" copies of the Software, and to permit persons to whom the Software is
" furnished to do so, subject to the following conditions:
"
" The above copyright notice and this permission notice shall be included in all
" copies or substantial portions of the Software.
"
" THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
" IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
" FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
" AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
" LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
" OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
" SOFTWARE.


" This is basic vim plugin boilerplate
let s:save_cpo = &cpo
set cpo&vim

function! s:restore_cpo()
  let &cpo = s:save_cpo
  unlet s:save_cpo
endfunction

if exists( "g:loaded_dyevim" )
  call s:restore_cpo()
  finish
elseif v:version < 704 || (v:version == 704 && !has('patch405'))
  echohl WarningMsg |
        \ echomsg "DyeVim unavailable: requires Vim 7.4.405+" |
        \ echohl None
  call s:restore_cpo()
  finish
elseif !has( 'python' ) && !has( 'python3' )
  echohl WarningMsg |
        \ echomsg "DyeVim unavailable: requires Vim compiled with " .
        \ "Python (2.6+ or 3.3+) support" |
        \ echohl None
  call s:restore_cpo()
  finish
elseif !exists( "g:loaded_youcompleteme" ) || g:loaded_youcompleteme != 1
  echohl WarningMsg |
        \ echomsg "DyeVim unavailable: requires YouCompleteMe plugin." |
        \ echohl None
  call s:restore_cpo()
  finish
endif

let g:loaded_dyevim = 1

" On-demand loading. Let's use the autoload folder and not slow down vim's
" startup procedure.
augroup dyeVimdye
  autocmd!
  autocmd VimEnter * call dyevim#Enable()
augroup END

" This is basic vim plugin boilerplate
call s:restore_cpo()
