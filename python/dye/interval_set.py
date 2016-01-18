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

    def __init__(self, *args):
        self._intervals = list( args )


    def __repr__(self):
        return "<IntervalSet: {0} >".format(tuple(self._intervals))


    def __iter__( self ):
        return self._intervals.__iter__()


    def __len__( self ):
        return len ( self._intervals )


    def __iand__( self, other ):
        b = bisect.bisect_left( self._intervals, other )
        e = bisect.bisect_right( self._intervals, other )
        if b == e:
            self._intervals = []
        else:
            del self._intervals[ : b - 1 ]
            self._intervals[ b ] &= other
            if e - b > 1:
                self._intervals[ e - 1 ] &= other
            del self._intervals[ e : ]

        return self


    def __and__( self, other ):
        result = copy.deepcopy( self )
        result &= other
        return result


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


    def _Normalize( self ):
        result = [ i for i in self._intervals if i ]
        self._intervals = result


    def __isub__( self, other ):
        if isinstance( other, IntervalSet ):
            raise "Not Supported."
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
