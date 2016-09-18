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

function! dyevim#ft#cpp#solarized#Setup()
    "throw 'Not implemented'
    "TODO add terminal support
    hi UserType guifg=#c17100
    hi Namespace guifg=#c17100 gui=italic
    hi MemberVar guifg=#6c71c4
    hi FunctionParam guifg=#93a1a1 gui=bold
    hi SkippedRange guifg=#657b83

    hi link Dye_cpp_Namespace Namespace
    hi link Dye_cpp_Class UserType
    hi link Dye_cpp_Struct UserType
    hi link Dye_cpp_Union UserType
    hi link Dye_cpp_MemberVariable MemberVar
    hi link Dye_cpp_Typedef UserType
    hi link Dye_cpp_TemplateType UserType
    hi link Dye_cpp_Enum UserType
    hi link Dye_cpp_EnumConstant Constant
    hi link Dye_cpp_PreprocessingDirective Macro
    hi link Dye_cpp_Macro Macro
    hi link Dye_cpp_Function Function
    hi link Dye_cpp_FunctionParam FunctionParam
    hi link Dye_cpp_SkippedRange SkippedRange
endfunction
