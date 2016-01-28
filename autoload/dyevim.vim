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

function! dyevim#Enable()
    if &diff
        return
    endif

    call s:SetupPython()
    call s:SetupSyntaxRules()
    call s:SetupAutocommands()
    call s:SetupWheelMappings()
    "call youcompleteme#RegisterSemanticTokensReadyPythonCallback(
    "    \ 'DyeVimSemanticTokensReady')
endfunction

function! s:SetupPython()
python << EOF
import sys

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
    augroup END
endfunction

function! s:OnCursorMoved()
    py dyevim_state.OnCursorMoved()
endfunction

function! s:SetupSyntaxRules()
    highlight NormalBold gui=bold
    highlight TypeBold ctermfg=121 guifg=#b58900 gui=bold
    highlight link Dye_Namespace Function
    highlight link Dye_Class TypeBold
    highlight link Dye_Struct TypeBold
    highlight link Dye_Union TypeBold
    highlight link Dye_MemberVariable Function
    highlight link Dye_Typedef TypeBold
    highlight link Dye_TemplateType TypeBold
    highlight link Dye_Enum TypeBold
    highlight link Dye_EnumConstant Constant
    highlight link Dye_Macro Macro
    highlight link Dye_Function Function
    highlight link Dye_FunctionParam NormalBold
endfunction

function! s:SetupWheelMappings()
    nnoremap <silent> <ScrollWheelUp>
                    \ <ScrollWheelUp>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <ScrollWheelUp>
                    \ <ScrollWheelUp><ESC>:call <SID>OnCursorMoved()<CR><INS>
    nnoremap <silent> <ScrollWheelDown>
                    \ <ScrollWheelDown>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <ScrollWheelDown>
                    \ <ScrollWheelDown><ESC>:call <SID>OnCursorMoved()<CR><INS>

    nnoremap <silent> <S-ScrollWheelUp>
                    \ <S-ScrollWheelUp>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <S-ScrollWheelUp>
                    \ <S-ScrollWheelUp><ESC>:call <SID>OnCursorMoved()<CR><INS>
    nnoremap <silent> <S-ScrollWheelDown>
                    \ <S-ScrollWheelDown>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <S-ScrollWheelDown>
                    \ <S-ScrollWheelDown><ESC>:call <SID>OnCursorMoved()<CR><INS>

    nnoremap <silent> <C-ScrollWheelUp>
                    \ <C-ScrollWheelUp>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <C-ScrollWheelUp>
                    \ <C-ScrollWheelUp><ESC>:call <SID>OnCursorMoved()<CR><INS>
    nnoremap <silent> <C-ScrollWheelDown>
                    \ <C-ScrollWheelDown>:call <SID>OnCursorMoved()<CR>
    inoremap <silent> <C-ScrollWheelDown>
                    \ <C-ScrollWheelDown><ESC>:call <SID>OnCursorMoved()<CR><INS>
endfunction

" This is basic vim plugin boilerplate
let &cpo = s:save_cpo
unlet s:save_cpo
