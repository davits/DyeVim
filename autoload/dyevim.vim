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


let s:save_cpo = &cpo
set cpo&vim

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\' )
let s:current_filetype = ''
let s:py = has('python3') ? "py3" : "py"
let s:python_eof = has('python3') ? "python3 << EOF" : "python << EOF"

function! dyevim#Enable()
    if &diff
        return
    endif

    if s:SetupPython() != 1
        return
    endif

    call s:SetupAutocommands()
    call s:SetupWheelMappings()

    call s:OnWindowEnter()
    call s:OnBufferEnter()
endfunction

function! s:SetupPython()
exec s:python_eof
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
import sys
import vim

script_folder = vim.eval( 's:script_folder_path' )
sys.path.insert( 0, os.path.join( script_folder, '../python' ) )

from dye.dyevim import DyeVim
try:
    dyevim_state = DyeVim( ycm_state )
except NameError:
    vim.command('return 0')
EOF
return 1
endfunction

function! s:SetupAutocommands()
    augroup dyevim
        autocmd!
        autocmd CursorMovedI * call s:OnCursorMoved()
        autocmd CursorMoved * call s:OnCursorMoved()

        autocmd WinEnter * call s:OnWindowEnter()
        autocmd BufEnter * call s:OnBufferEnter()

        autocmd FileType * call s:OnSetFileType()
    augroup END
endfunction

function! s:OnCursorMoved()
    exec s:py "dyevim_state.OnCursorMoved()"
    " Return empty string for <C-R> mapping
    return ''
endfunction

function! s:OnWindowEnter()
    exec s:py "dyevim_state.OnWindowEnter()"
endfunction

function! s:OnBufferEnter()
    exec s:py "dyevim_state.OnBufferEnter()"
endfunction

function! s:OnSetFileType()
    exec s:py "dyevim_state.OnFileTypeChanged()"
endfunction

function! s:SetupWheelMappings()
    nnoremap <silent> <ScrollWheelUp>
                    \ <ScrollWheelUp>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <ScrollWheelUp>
                    \ <ScrollWheelUp><C-R>=<SID>OnCursorMoved()<CR>
    nnoremap <silent> <ScrollWheelDown>
                    \ <ScrollWheelDown>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <ScrollWheelDown>
                    \ <ScrollWheelDown><C-R>=<SID>OnCursorMoved()<CR>

    nnoremap <silent> <S-ScrollWheelUp>
                    \ <S-ScrollWheelUp>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <S-ScrollWheelUp>
                    \ <S-ScrollWheelUp><C-R>=<SID>OnCursorMoved()<CR>
    nnoremap <silent> <S-ScrollWheelDown>
                    \ <S-ScrollWheelDown>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <S-ScrollWheelDown>
                    \ <S-ScrollWheelDown><C-R>=<SID>OnCursorMoved()<CR>

    nnoremap <silent> <C-ScrollWheelUp>
                    \ <C-ScrollWheelUp>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <C-ScrollWheelUp>
                    \ <C-ScrollWheelUp><C-R>=<SID>OnCursorMoved()<CR>
    nnoremap <silent> <C-ScrollWheelDown>
                    \ <C-ScrollWheelDown>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <C-ScrollWheelDown>
                    \ <C-ScrollWheelDown><C-R>=<SID>OnCursorMoved()<CR>
endfunction

" This is basic vim plugin boilerplate
let &cpo = s:save_cpo
unlet s:save_cpo
