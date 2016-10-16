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

function! dyevim#ft#cpp#wombat256mod#Setup()
    "TODO add terminal support
    hi Namespace guifg=#e0c477 gui=italic
    hi UserType guifg=#e0c477
    hi MemberVariable guifg=#98c845
    hi StaticMemberVariable guifg=#98c845 gui=italic
    hi Variable guifg=#e3e0d7 gui=italic
    hi MemberFunction guifg=#cae982
    hi StaticMemberFunction guifg=#cae982 gui=italic
    hi link DyeFunction Function
    hi FunctionParameter guifg=#e3e0d7 gui=bold
    hi link Enumerator Constant
    hi link DyeMacro Macro
    hi SkippedRange guifg=#9c998e
endfunction
