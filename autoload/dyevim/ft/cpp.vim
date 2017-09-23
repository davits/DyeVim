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

function! dyevim#ft#cpp#Setup()
    try
        exec 'call dyevim#ft#cpp#' . g:colors_name . '#Setup()'
    catch
        call dyevim#ft#cpp#GenericSetup()
    endtry

    call dyevim#colors#CreateBoldVariant( 'ConstantBold', 'Constant' )
    hi link Dye_cpp_Namespace Namespace
    hi link Dye_cpp_Class UserType
    hi link Dye_cpp_Structure UserType
    hi link Dye_cpp_Union UserType
    hi link Dye_cpp_TypeAlias UserType
    hi link Dye_cpp_MemberVariable MemberVariable
    hi link Dye_cpp_StaticMemberVariable StaticMemberVariable
    hi link Dye_cpp_GlobalVariable GlobalVariable
    hi link Dye_cpp_Variable Variable
    hi link Dye_cpp_MemberFunction MemberFunction
    hi link Dye_cpp_StaticMemberFunction StaticMemberFunction
    hi link Dye_cpp_Function DyeFunction
    hi link Dye_cpp_FunctionParameter FunctionParameter
    hi link Dye_cpp_Enumeration ConstantBold
    hi link Dye_cpp_Enumerator Enumerator
    hi link Dye_cpp_TemplateParameter UserType
    hi link Dye_cpp_TemplateNonTypeParameter FunctionParameter
    hi link Dye_cpp_PreprocessingDirective DyeMacro
    hi link Dye_cpp_Macro DyeMacro
    hi link Dye_cpp_SkippedRange SkippedRange

endfunction


function! dyevim#ft#cpp#GenericSetup()
    call dyevim#colors#CreateBoldVariant( 'NormalBold', 'Normal' )
    call dyevim#colors#CreateItalicVariant( 'NormalItalic', 'Normal' )
    call dyevim#colors#CreateBoldVariant( 'TypeBold', 'Type' )
    call dyevim#colors#CreateBoldVariant( 'FunctionBold', 'Function' )
    call dyevim#colors#CreateItalicVariant( 'TypeItalic', 'Type' )

    hi link Namespace TypeItalic
    hi link UserType TypeBold
    hi link MemberVariable FunctionBold
    hi link StaticMemberVariable FunctionBold
    hi link GlobalVariable NormalItalic
    hi link Variable Normal
    hi link MemberFunction Function
    hi link StaticMemberFunction Function
    hi link DyeFunction Function
    hi link FunctionParameter NormalBold
    hi link Enumerator Constant
    hi link DyeMacro Macro
    hi link SkippedRange cCppOutSkip
endfunction
