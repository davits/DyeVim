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

import bisect
import copy
import sys

class IntervalSet( object ):

    def __init__( self, *args ):
        self._intervals = []
        for i in args:
            self |= i


    def __repr__( self ):
        return "IntervalSet: [ {0} ]".format( tuple( self._intervals ) )


    def __eq__( self, other ):
        return self._intervals == other._intervals


    def __iter__( self ):
        return self._intervals.__iter__()


    def __len__( self ):
        return len( self._intervals )


    def __contains__( self, other ):
        if isinstance( other, IntervalSet ):
            raise TypeError( 'Invalid argument type for in operator.' )
        b = bisect.bisect_left( self._intervals, other )
        e = bisect.bisect_right( self._intervals, other )
        if e - b == 1:
            return other in self._intervals[ b ]
        return False


    def __ior__( self, other ):
        if isinstance( other, IntervalSet ):
            for i in other:
                self |= i
            return self
        else:
            b = bisect.bisect_left( self._intervals, other )
            e = bisect.bisect_right( self._intervals, other )
            if b == e:
                u = copy.copy( other )
            else:
                u = self._intervals[ b ] | other
                if e - b > 1:
                    u |= self._intervals[ e - 1 ]

            if b > 0:
                prev = self._intervals[ b - 1 ]
                if prev.end + 1 == u.begin:
                    u.begin = prev.begin
                    b -= 1
            if e < len( self ):
                nxt = self._intervals[ e ]
                if u.end + 1 == nxt.begin:
                    u.end = nxt.end
                    e += 1

            self._intervals[ b : e ] = u
            return self


    def __or__( self, other ):
        result = copy.deepcopy( self )
        result |= other
        return result


    def __iand__( self, other ):
        if isinstance( other, IntervalSet ):
            raise TypeError( 'Invalid argument type for & operator.' )
        b = bisect.bisect_left( self._intervals, other )
        e = bisect.bisect_right( self._intervals, other )
        if b == e:
            self._intervals = []
            return self
        self._intervals[ b ] &= other
        if e - b > 1:
            self._intervals[ e - 1 ] &= other
        del self._intervals[ e : ]
        del self._intervals[ : b ]
        return self


    def __and__( self, other ):
        result = copy.deepcopy( self )
        result &= other
        return result


    def _Normalize( self ):
        result = [ i for i in self._intervals if i ]
        self._intervals = result


    def __isub__( self, other ):
        if isinstance( other, IntervalSet ):
            raise TypeError( 'Invalid argument type for - operator.' )
        b = bisect.bisect_left( self._intervals, other )
        e = bisect.bisect_right( self._intervals, other )
        if b == e:
            return self
        if e - b > 1:
            s = self._intervals[ e - 1 ] - other
            self._intervals[ e : e ] = s

        s = self._intervals[ b ] - other
        self._intervals[ b : e ] = s
        self._Normalize()
        return self


    def __sub__( self, other ):
        result = copy.deepcopy( self )
        result -= other
        return result


    def GetIntervalForQuery( self, interval, size ):
        if not self._intervals:
            return copy.copy( interval ).EnlargeBottomTo( size )

        b = bisect.bisect_left( self._intervals, interval )
        e = bisect.bisect_right( self._intervals, interval )
        if e - b > 1:
            return self._GetQueryIntervalMulti( interval, size, b, e )
        elif e - b == 1:
            return self._GetQueryIntervalSingle( interval, size, b, e )
        else:
            return self._GetQueryInterval( interval, size, b )


    # Get best query range when there are intersections with multiple intervals
    def _GetQueryIntervalMulti( self, interval, size, b, e ):
        result = interval - self
        if interval.begin not in self._intervals[ b ]:
            result._intervals[ 0 ].EnlargeTopTo( size )
            if b != 0:
                result._intervals[ 0 ] -= self._intervals[ b - 1 ]
        if interval.end not in self._intervals[ e - 1 ]:
            result._intervals[ -1 ].EnlargeBottomTo( size )
            if e < len( self._intervals ):
                result._intervals[ -1 ] -= self._intervals[ e ]
        return result


    # Get best query range when there is an intersection with single interval
    def _GetQueryIntervalSingle( self, interval, size, b, e ):
        result = interval - self._intervals[ b ]
        if interval.begin in self._intervals[ b ]:
            result.EnlargeBottomTo( size )
            if e < len( self._intervals ):
                result -= self._intervals[ e ]
        if interval.end in self._intervals[ b ]:
            result.EnlargeTopTo( size )
            if b != 0:
                result -= self._intervals[ b - 1 ]
        return result


    # Get best query range when there are no intersections
    def _GetQueryInterval( self, interval, size, b ):
        top = 1
        if b != 0:
            top = self._intervals[ b - 1 ].end + 1
        if b < len( self._intervals ):
            bottom = self._intervals[ b ].begin - 1
        else:
            bottom = sys.maxint
        result = copy.copy( interval )
        result.EnlargeBottomTo( size )
        if result.end > bottom:
            result.MoveUpBy( result.end - bottom )
            # Interval can't be moved upper then 1
            if result.end > bottom:
                result.end = bottom
            if result.begin < top:
                result.begin = top
        if result.begin < top:
            result.MoveDownBy( top - result.begin )
            if result.end > bottom:
                result.end = bottom
        return result
