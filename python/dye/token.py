#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Davit Samvelyan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import vim

class Token( object ):

    def __init__( self, filetype, value ):
        group = 'Dye_{0}_{1}'.format( filetype, value[ 'kind' ] )
        line = value[ 'line_number' ]
        column = value[ 'column_number' ]
        offset = value[ 'offset' ]

        self.line = line
        self._matchIds = {}
        self._create = ( 'matchaddpos("{0}", [[{1}, {2}, {3}]], -1)'
                         .format( group, line, column, offset ) )


    def __lt__( self, line ):
        return self.line < line


    def __gt__( self, line ):
        return self.line > line


    def AddMatch( self, wid ):
        if wid not in self._matchIds:
            self._matchIds[ wid ] = vim.eval( self._create )


    def RemoveMatch( self, wid ):
        matchId = self._matchIds.pop( wid, 0 )
        if matchId != 0:
            vim.command( 'call matchdelete({0})'.format( matchId ) )
