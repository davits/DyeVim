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

from .interval import Interval

import vim

class Token( object ):

    def __init__( self, filetype, range, type ):

        start = range[ 'start' ]
        end = range[ 'end' ]
        start_line = start[ 'line_num' ]
        start_col = start[ 'column_num' ]
        end_line = end[ 'line_num' ]
        end_col = end[ 'column_num' ]
        group = 'Dye_{0}_{1}'.format( filetype, type )

        self.range = Interval( start_line, end_line )
        self._matchIds = {}
        self._create = self._GetTokenCreateStr( group,
                                                start_line, start_col,
                                                end_line, end_col )


    def __lt__( self, line ):
        return self.range < line


    def __gt__( self, line ):
        return self.range > line


    def _GetTokenCreateStr( self, group,
                            start_line, start_column,
                            end_line, end_column ):
        if start_line == end_line:
            return ( 'matchaddpos("{0}", [[{1}, {2}, {3}]], -1)'
                      .format( group, start_line, start_column,
                               end_column - start_column ) )

        regex = '\%{0}l\%>{1}c\|'.format( start_line, start_column - 1 )
        if end_line - start_line > 1:
            regex += '\%>{0}l\%<{1}l\|'.format( start_line, end_line )
        regex += '\%{0}l\%<{1}c'.format( end_line, end_column + 1 )

        return 'matchadd("{0}", \'{1}\', -1)'.format( group, regex )


    def AddMatch( self, wid ):
        if wid not in self._matchIds:
            self._matchIds[ wid ] = vim.eval( self._create )


    def RemoveMatch( self, wid ):
        matchId = self._matchIds.pop( wid, 0 )
        if matchId != 0:
            vim.command( 'call matchdelete({0})'.format( matchId ) )
