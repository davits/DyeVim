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
            if prev._end + 1 == u._begin:
                u._begin = prev._begin
                b -= 1
        if e < len( self ):
            nxt = self._intervals[ e ]
            if u._end + 1 == nxt._begin:
                u._end = nxt._end
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
            return IntervalSet()
        self._intervals[ b ] &= other
        if b - e > 1:
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
            result = interval - self
            if interval._begin not in self._intervals[ b ]:
                result._intervals[ 0 ].EnlargeTopTo( size )
                if b != 0:
                    result._intervals[ 0 ] -= self._intervals[ b - 1 ]
            if interval._end not in self._intervals[ e - 1 ]:
                result._intervals[ -1 ].EnlargeBottomTo( size )
                if e < len( self._intervals ):
                    result._intervals[ -1 ] -= self._intervals[ e ]
        elif e - b == 1:
            result = interval - self._intervals[ b ]
            if interval._begin in self._intervals[ b ]:
                result.EnlargeBottomTo( size )
                if e < len( self._intervals ):
                    result -= self._intervals[ e ]
            if interval._end in self._intervals[ b ]:
                result.EnlargeTopTo( size )
                if b != 0:
                    result -= self._intervals[ b - 1 ]
        else:
            top = 1
            if b != 0:
                top = self._intervals[ b - 1 ]._end + 1
            if e < len( self._intervals ):
                bottom = self._intervals[ e ]._begin - 1
            else:
                bottom = interval._begin + size - 1
            result = copy.copy( interval )
            result.EnlargeBottomTo( size )
            if result._end > bottom:
                result.MoveUpBy( result._end - bottom )
                if result._begin < top:
                    result._begin = top
            if result._begin < top:
                result.MoveDownBy( top - result._begin )
                if result._end > bottom:
                    result._end = bottom

        return result
