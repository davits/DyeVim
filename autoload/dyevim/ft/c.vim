" The MIT License (MIT)
"
" Copyright (c) 2017 Davit Samvelyan
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

function! dyevim#ft#c#Setup()
    try
        exec 'call dyevim#ft#c#' . g:colors_name . '#Setup()'
    catch
        call dyevim#ft#cpp#GenericSetup()
    endtry

    call dyevim#colors#CreateBoldVariant( 'ConstantBold', 'Constant' )
    hi link Dye_c_Namespace Namespace
    hi link Dye_c_Class UserType
    hi link Dye_c_Structure UserType
    hi link Dye_c_Union UserType
    hi link Dye_c_TypeAlias UserType
    hi link Dye_c_MemberVariable MemberVariable
    hi link Dye_c_StaticMemberVariable StaticMemberVariable
    hi link Dye_c_GlobalVariable GlobalVariable
    hi link Dye_c_Variable Variable
    hi link Dye_c_MemberFunction MemberFunction
    hi link Dye_c_StaticMemberFunction StaticMemberFunction
    hi link Dye_c_Function DyeFunction
    hi link Dye_c_FunctionParameter FunctionParameter
    hi link Dye_c_Enumeration ConstantBold
    hi link Dye_c_Enumerator Enumerator
    hi link Dye_c_TemplateParameter UserType
    hi link Dye_c_TemplateNonTypeParameter FunctionParameter
    hi link Dye_c_PreprocessingDirective DyeMacro
    hi link Dye_c_Macro DyeMacro
    hi link Dye_c_SkippedRange SkippedRange

endfunction
