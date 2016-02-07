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
from token import Token
import log

import bisect

import vim

class Buffer( object ):

    def __init__( self, bufnr, ycm ):
        self.number = bufnr
        self._ycm = ycm
        self._tokens = []
        self._covered = IntervalSet(  )


    def Reset( self ):
        self._tokens = []
        self._covered = IntervalSet()


    def GetTokens( self, interval, request = True ):
        if not request:
            return self._GetTokens( interval )

        if interval in self._covered:
            return self._GetTokens( interval )

        query_intervals = self._covered.GetIntervalForQuery( interval,
                                                             Viewport.Size() )
        for qi in query_intervals:
            self._QueryAndStore( qi )

        return self._GetTokens( interval )


    def _GetTokens( self, interval ):
        b = bisect.bisect_left( self._tokens, interval.begin )
        e = bisect.bisect_right( self._tokens, interval.end )
        return self._tokens[ b : e ]


    def _QueryAndStore( self, interval ):
        tokens = self._QueryTokens( interval )
        if not isinstance( tokens, list ):
            return
        b = bisect.bisect_left( self._tokens, interval.begin )
        e = bisect.bisect_right( self._tokens, interval.end )
        self._tokens[ b : e ] = tokens
        self._covered |= interval


    def _QueryTokens( self, interval ):
        log.debug( 'Querying tokens for buffer {0}, interval {1}'
                    .format( self.number, interval ) )
        token_dicts = self._ycm.GetSemanticTokens( self.number,
                                                   interval.begin, 1,
                                                   interval.end + 1, 1,
                                                   0.01 )
        if isinstance( token_dicts, str ):
            if token_dicts == 'Timeout':
                # message
                pass
            return False

        ft = vim.buffers[ self.number ].options[ 'filetype' ]
        return [ Token( ft, x ) for x in token_dicts ]
