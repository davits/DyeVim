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

from .interval.interval import Interval
from .interval.interval_set import IntervalSet
from .token import Token
from .utils import log, viewport, vimsupport
from .utils.range import Range

import bisect

class Buffer( object ):

    def __init__( self, bufnr, ycm ):
        self.number = bufnr
        self._ycm = ycm
        self._tokens = []
        self._covered = IntervalSet()
        self._skipped_ranges = IntervalSet()
        self._sr_tokens = [] # Tokens for skipped ranges
        self._sr_queried = False
        # TODO move into separate options with second option
        self._timeout = vimsupport.GetIntValue( 'g:dyevim_timeout' ) / 1000


    def Reset( self ):
        self._tokens = []
        self._covered = IntervalSet()
        self._skipped_ranges = IntervalSet()
        self._sr_tokens = []
        self._sr_queried = False


    def GetTokens( self, interval, request = True ):
        log.debug( 'GetTokens from buffer {0}, interval {1}'
                   .format( self.number, interval ) )
        if not request or interval in self._covered:
            return self._GetIntervalTokens( self._tokens, interval )

        query_intervals = self._covered.GetIntervalForQuery( interval,
                                                             viewport.Size() )
        for qi in query_intervals:
            qi.LimitBottomBy( vimsupport.GetBufferLen( self.number ) )
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
        skipped_ranges = self._ycm.GetSkippedRanges( self.number,
                                                     self._timeout )

        if not isinstance( skipped_ranges, list ):
            log.debug( "Query Error {0}".format( skipped_ranges ) )
            if skipped_ranges == 'Timeout':
                bufName = vimsupport.BufNumberToName( self.number )
                vimsupport.PostVimWarning( "Skipped range query timeout for "
                                           "buffer {0}".format( bufName ) )
            return

        ft = vimsupport.GetFileType( self.number )
        tokens = []
        for sr_dict in skipped_ranges:
            sr = Range( sr_dict )
            self._skipped_ranges |= Interval( sr.start.line, sr.end.line )
            tokens.extend( Token.CreateTokens( ft, 'SkippedRange', sr, 11 ) )

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

        end_col = vimsupport.GetLineLen( self.number, interval.end ) + 1
        token_dicts = self._ycm.GetSemanticTokens( self.number,
                                                   interval.begin, 1,
                                                   interval.end, end_col,
                                                   self._timeout )
        if not isinstance( token_dicts, list ):
            log.debug( "Query Error {0}".format( token_dicts ) )
            if token_dicts == 'Timeout':
                bufName = vimsupport.BufNumberToName( self.number )
                vimsupport.PostVimWarning( "Token query timeout for buffer "
                                           "{0} interval {1}"
                                           .format( bufName, interval ) )
            return False

        ft = vimsupport.GetFileType( self.number )
        tokens = []
        for td in token_dicts:
            tk = td[ 'kind' ]
            tt = td[ 'type' ]
            if tk == 'Identifier' and tt != 'Unsupported':
                tr = Range( td[ 'range' ] )
                tokens.extend( Token.CreateTokens( ft, tt, tr ) )

        # Sometimes clang may return tokens on neighboring lines.
        tokens = self._GetIntervalTokens( tokens, interval )
        # Remove tokens on skipped ranges lines
        for r in ( interval & self._skipped_ranges ):
            ( b, e ) = self._Bisect( tokens, r )
            del tokens[ b : e ]

        return tokens


    def _GetIntervalTokens( self, tokens, interval ):
        ( b, e ) = self._Bisect( tokens, interval )
        return tokens[ b : e ]


    def _Bisect( self, tokens, interval ):
        b = bisect.bisect_left( tokens, interval.begin )
        e = bisect.bisect_right( tokens, interval.end )
        return ( b, e )
