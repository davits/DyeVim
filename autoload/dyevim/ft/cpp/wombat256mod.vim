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
    "throw 'Not implemented'
    "TODO add terminal support
    hi UserType guifg=#e0c477
    hi Namespace guifg=#e0c477 gui=italic
    hi MemberVar guifg=#98c845
    hi Variable guifg=#e3e0d7 gui=italic
    hi FunctionParam guifg=#e3e0d7 gui=bold
    hi SkippedRange guifg=#9c998e

    hi link Dye_cpp_Namespace Namespace
    hi link Dye_cpp_Class UserType
    hi link Dye_cpp_Struct UserType
    hi link Dye_cpp_Union UserType
    hi link Dye_cpp_TypeAlias UserType
    hi link Dye_cpp_MemberVariable MemberVar
    hi link Dye_cpp_Variable Variable
    hi link Dye_cpp_Function Function
    hi link Dye_cpp_FunctionParameter FunctionParam
    hi link Dye_cpp_Enumeration UserType
    hi link Dye_cpp_Enumerator Constant
    hi link Dye_cpp_TemplateParameter UserType
    hi link Dye_cpp_TemplateNonTypeParameter FunctionParam
    hi link Dye_cpp_PreprocessingDirective Macro
    hi link Dye_cpp_Macro Macro
    hi link Dye_cpp_SkippedRange SkippedRange
endfunction
