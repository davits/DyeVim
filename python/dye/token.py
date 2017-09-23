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

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import vim

class Token( object ):

    @staticmethod
    def CreateTokens( file_type, token_type, tr, priority = -1 ):
        if tr.SingleLine():
            return [ Token( file_type, token_type, priority,
                            tr.start.line, tr.start.column, tr.Offset() ) ]

        tokens = [ Token( file_type, token_type, priority,
                          tr.start.line, tr.start.column ) ]

        for line in range( tr.start.line + 1, tr.end.line ):
            tokens.append( Token( file_type, token_type, priority, line ) )

        tokens.append( Token( file_type, token_type, priority,
                              tr.end.line, 1, tr.end.column - 1 ) )
        return tokens


    def __init__( self, file_type, token_type, priority,
                  line, column = None, offset = None):

        group = 'Dye_{0}_{1}'.format( file_type, token_type )

        self.line = line
        self._matchIds = {}
        self._create = self._GetTokenCreateStr( group, priority,
                                                line, column, offset )


    def __lt__( self, line ):
        return self.line < line


    def __gt__( self, line ):
        return self.line > line


    def _GetTokenCreateStr( self, group, priority, line, column, offset ):
        if offset is not None:
            return ( 'matchaddpos("{0}", [[{1}, {2}, {3}]], {4})'
                     .format( group, line, column, offset, priority ) )

        if column is not None:
            regex = '\%{0}l\%>{1}c'.format( line, column - 1 )
            return ( 'matchadd("{0}", \'{1}\', {2})'
                     .format( group, regex, priority ) )

        return ( 'matchaddpos("{0}", [[{1}]], {2})'
                 .format( group, line, priority ) )



    def __repr__( self ):
        return "Token {0}".format( self._create )


    def AddMatch( self, wid ):
        if wid not in self._matchIds:
            self._matchIds[ wid ] = vim.eval( self._create )


    def RemoveMatch( self, wid ):
        matchId = self._matchIds.pop( wid, 0 )
        if matchId != 0:
            vim.command( 'call matchdelete({0})'.format( matchId ) )
