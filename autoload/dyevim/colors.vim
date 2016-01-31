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


function! dyevim#colors#CreateBoldVariant( newGroup, linkedGroup )
    let details = s:GroupDetails( a:linkedGroup )
    exe printf( 'hi %s %s gui=bold', a:newGroup, details )
endfunction

function! dyevim#colors#CreateItalicVariant( newGroup, linkedGroup )
    let details = s:GroupDetails( a:linkedGroup )
    exe printf( 'hi %s %s gui=italic', a:newGroup, details )
endfunction

function! dyevim#colors#CreateUnderlinedVariant( newGroup, linkedGroup )
    let details = s:GroupDetails( a:linkedGroup )
    exe printf( 'hi %s %s gui=underline', a:newGroup, details )
endfunction

function! s:GroupDetails( name )
    " Redirect the output of the "hi" command into a variable
    " and find the highlighting
    redir => details
    exe 'silent hi ' . a:name
    redir END
    let details = substitute( details, "\n", '', 'g' )

    if details !~ 'links to'
        let index = stridx( details, ' xxx ' )
        let details = strpart( details, index + 5 )
        return s:RemoveFontComponent( details )
    endif

    " Resolve linked groups to find the root highlighting scheme
    let index = strridx( details, ' ' )
    let linked = strpart( details, index + 1 )
    return s:GroupDetails( linked )
endfunction

function! s:RemoveFontComponent( details )
    " Remove font=value if exists
    let index = stridx( a:details, 'font=' )
    if index != -1
        let next_idx = stridx( a:details, '=', index + 5 )
        if next_idx == -1
            return strpart( a:details, 0, index )
        else
            let next_idx = strridx( a:details, ' ', next_idx )
            return strpart( a:details, 0, index ) .
                 \ strpart( a:details, next_idx )
        endif
    endif
    return a:details
endfunction
