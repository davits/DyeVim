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


from viewport import Viewport
from token_provider import TokenProvider

import bisect

class Buffer( object ):

    def __init__( self, bufnr, ycm ):
        self._tp = TokenProvider( bufnr, ycm )
        self._viewport = Viewport.Current()


    def OnUpdateTokens( self ):
        self._RemoveMatchesFromViewport( self._viewport )
        self._tp.Reset()
        self._CreateMatchesForViewport( self._viewport )


    def _CreateMatchesForViewport( self, view ):
        for token in self._tp.GetTokens( view ):
            token.AddMatch()


    def _RemoveMatchesFromViewport( self, view ):
        for token in self._tp.GetTokens( view, False ):
            token.RemoveMatch()


    def OnCursorMoved( self ):
        current = Viewport.Current(  )
        if self._viewport != current:
            self.OnViewportChanged( current )


    def OnViewportChanged( self, current ):
        remove_views = self._viewport - current
        for view in remove_views:
            self._RemoveMatchesFromViewport( view )

        apply_views = current - self._viewport
        for view in apply_views:
            self._CreateMatchesForViewport( view )

        self._viewport = current


    def OnLineInserted( self, line, count ):
        self._RemoveMatchesFromViewport( Viewport( line, self._viewport.end ) )

        line_index = bisect.bisect_left( self._tokens, line )
        for i in range( line_index, len( self._tokens ) ):
            self._tokens[i].line += count

        self._CreateMatchesForViewport( Viewport( line + count, self._viewport.end ) )


    def OnLineRemoved( self, line, count ):
        self._RemoveMatchesFromViewport( Viewport( line, self._viewport.end ) )

        end = line + count - 1
        token_range = self._GetTokensRangeForViewport( Viewport( line, end ) )
        del self._tokens[token_range[0] : token_range[1]]

        end_index = bisect.bisect_right( self._tokens, end )
        for i in range( end_index, len( self._tokens ) ):
            self._tokens[i].line -= count

        self._CreateMatchesForViewport( Viewport( line, self._viewport.end ) )

