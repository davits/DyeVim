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

class Interval( object ):

    def __init__( self, b, e ):
        self._begin = b
        self._end = e


    def __eq__( self, other ):
        return ( self._begin == other._begin and
                 self._end == other._end )


    def __ne__( self, other ):
        return not ( self == other )


    def __lt__( self, other ):
        return self._end < other._begin


    def __gt__( self, other ):
        return self._begin > other._end


    def __len__( self ):
        l = self._end - self._begin + 1
        return l if l > 0 else 0


    def __contains__( self, other ):
        if isinstance( other, Interval ):
            return other._begin >= self._begin and other._end <= self._end
        return other >= self._begin and other <= self._end


    def Empty( self ):
        return self._begin > self._end


    def Overlaps( self, other ):
        return not ( self < other ) and not ( self > other )


    def __sub__( self, other ):
        # TODO fix this
        if self in other:
            return Interval
        b = other._begin in self
        e = other._end in self
        if b and e:
            return IntervalSet( Interval( self._begin, other._begin - 1 ),
                                Interval( other._end + 1, self._end ) )
        elif b:
            return Interval( self._begin, other._begin - 1 )
        elif e:
            return Interval( other._end + 1, self._end )
        else:
            return self


    def __add__( self, other ):
        pass


    def __or__( self, other ):
        pass


    def __and__( self, other ):
        pass
