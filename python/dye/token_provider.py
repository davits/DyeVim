#!/usr/bin/env python
#
# The MIT License ( MIT )
#
# Copyright ( c ) 2016 Davit Samvelyan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files ( the "Software" ), to deal
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

from interval_set import IntervalSet
from viewport import Viewport

import bisect

class TokenProvider( object ):

    def __init__( self, bufnr ):
        self._bufnr = bufnr
        self._tokens = []
        self._covered = IntervalSet(  )


    def UpdateTokens( self, lr ):
        self._tokens = []
        self._covered = IntervalSet(  )


    def GetTokens( self, interval ):
        if interval in self._covered:
            return self._GetTokens( interval )
        query_intervals = self._covered.GetIntervalForQuery( interval,
                                                             Viewport.Size() )
        for qi in query_intervals:
            self_QueryAndStore( qi )

        return self._GetTokens( interval )


    def _GetTokens( self, interval ):
        b = bisect.bisect_left( self._tokens, interval._begin )
        e = bisect.bisect_right( self._tokens, interval._end )
        return self._tokens[ b : e ]


    def _QueryTokens( self, lr ):
        tokens = self._extractor.GetSemanticTokens( lr.begin, lr.end )
