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

from .utils import log, viewport

class Window( object ):

    def __init__( self, wid, buffer ):
        self._wid = wid
        self._buffer = buffer
        self._viewport = viewport.Current()


    def OnUpdateTokens( self ):
        self._RemoveMatchesFromInterval( self._viewport )
        self._buffer.Reset()
        self._CreateMatchesForInterval( self._viewport )


    def OnBufferChanged( self, buffer ):
        self._RemoveMatchesFromInterval( self._viewport )
        self._buffer = buffer
        self._CreateMatchesForInterval( self._viewport )


    def ClearWindow( self ):
        self._RemoveMatchesFromInterval( self._viewport )


    def _CreateMatchesForInterval( self, view ):
        for sr in self._buffer.GetSkippedRanges( view ):
            sr.AddMatch( self._wid )

        for token in self._buffer.GetTokens( view ):
            token.AddMatch( self._wid )


    def _RemoveMatchesFromInterval( self, view ):
        for sr in self._buffer.GetSkippedRanges( view, False ):
            sr.RemoveMatch( self._wid )

        for token in self._buffer.GetTokens( view, False ):
            token.RemoveMatch( self._wid )


    def OnCursorMoved( self ):
        current = viewport.Current()
        if self._viewport != current:
            self.OnViewportChanged( current )


    def OnViewportChanged( self, current ):
        log.debug( "Viewport Changed {0} -> {1}"
                   .format( self._viewport, current ) )
        remove_views = self._viewport - current
        for view in remove_views:
            self._RemoveMatchesFromInterval( view )

        apply_views = current - self._viewport
        for view in apply_views:
            self._CreateMatchesForInterval( view )

        self._viewport = current
