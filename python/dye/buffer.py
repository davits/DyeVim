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

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from .interval_set import IntervalSet
from .viewport import Viewport
from .token import Token
from . import log

import bisect

import vim

class Buffer( object ):

    def __init__( self, bufnr, ycm ):
        self.number = bufnr
        self._ycm = ycm
        self._tokens = []
        self._covered = IntervalSet(  )
        self._sr_tokens = [] # Tokens for skipped ranges
        self._sr_queried = False


    def Reset( self ):
        self._tokens = []
        self._covered = IntervalSet()
        self._sr_tokens = []
        self._sr_queried = False


    def GetTokens( self, interval, request = True ):
        log.debug( 'GetTokens from buffer {0}, interval {1}'
                   .format( self.number, interval ) )
        if not request or interval in self._covered:
            return self._GetIntervalTokens( self._tokens, interval )

        query_intervals = self._covered.GetIntervalForQuery( interval,
                                                             Viewport.Size() )
        for qi in query_intervals:
            qi.LimitBottomBy( self._GetBufferSize() )
            self._QueryTokensAndStore( qi )

        return self._GetIntervalTokens( self._tokens, interval )


    def GetSkippedRanges( self, interval, request = True ):
        log.debug( 'GetSkippedRanges from buffer {0}, interval {1}'
                   .format( self.number, interval ) )
        if not request or self._sr_queried:
            return self._GetIntervalTokens( self._sr_tokens, interval )

        self._QuerySkippedRanges()

        return self._GetIntervalTokens( self._sr_tokens, interval )


    def _QuerySkippedRanges( self ):
        log.info( 'Querying skipped ranges for buffer {0}'
                  .format( self.number ) )
        skipped_ranges = self._ycm.GetSkippedRanges( self.number, 0.01 )

        if not isinstance( skipped_ranges, list ):
            if skipped_ranges == 'Timeout':
                # message
                pass
            return

        ft = self._GetFileType()
        tokens = []
        for sr in skipped_ranges:
            tokens.extend( Token.CreateTokens( ft, 'SkippedRange', sr ) )

        self._sr_tokens = tokens
        self._sr_queried = True


    def _QueryTokensAndStore( self, interval ):
        tokens = self._QueryTokens( interval )
        if not isinstance( tokens, list ):
            return
        ( b, e ) = self._Bisect( self._tokens, interval )
        self._tokens[ b : e ] = tokens
        self._covered |= interval


    def _QueryTokens( self, interval ):
        log.info( 'Querying tokens for buffer {0}, interval {1}'
                    .format( self.number, interval ) )
        end_col = self._GetLineSize( interval.end - 1 )
        token_dicts = self._ycm.GetSemanticTokens( self.number,
                                                   interval.begin, 1,
                                                   interval.end, end_col,
                                                   0.01 )
        if not isinstance( token_dicts, list ):
            if token_dicts == 'Timeout':
                # message
                pass
            return False

        ft = self._GetFileType()
        tokens = []
        for td in token_dicts:
            tk = td[ 'kind' ]
            tt = td[ 'type' ]
            if tk == 'Identifier' and tt != 'Unsupported':
                tr = td[ 'range' ]
                tokens.extend( Token.CreateTokens( ft, tt, tr ) )

        # Sometimes clang may return tokens on neighboring lines.
        return self._GetIntervalTokens( tokens, interval )


    def _GetIntervalTokens( self, tokens, interval ):
        ( b, e ) = self._Bisect( tokens, interval )
        return tokens[ b : e ]


    def _Bisect( self, tokens, interval ):
        b = bisect.bisect_left( tokens, interval.begin )
        e = bisect.bisect_right( tokens, interval.end )
        return ( b, e )


    def _GetFileType( self ):
        return vim.buffers[ self.number ].options[ 'filetype' ]


    def _GetBufferSize( self ):
        return len( vim.buffers[ self.number ] )


    def _GetLineSize( self, line ):
        return len( vim.buffers[ self.number ][ line ] ) + 1
