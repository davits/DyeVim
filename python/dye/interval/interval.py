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

import copy

class Interval( object ):

    def __init__( self, b, e ):
        self.begin = b
        self.end = e


    def __repr__(self):
        return '[{0}, {1}]'.format( self.begin, self.end )


    def __eq__( self, other ):
        return ( self.TopAligns( other ) and
                 self.BottomAligns( other ) )


    def __ne__( self, other ):
        return not ( self == other )


    def __lt__( self, other ):
        if isinstance( other, ( int, long ) ):
            return self.end < other
        return self.end < other.begin


    def __gt__( self, other ):
        if isinstance( other, ( int, long ) ):
            return self.begin > other
        return self.begin > other.end


    def __nonzero__( self ):
        return self.__bool__()


    def __bool__( self ):
        return self.begin > 0 and self.begin <= self.end


    def __len__( self ):
        return self.end - self.begin + 1


    def __iter__( self ):
        if self:
            yield self


    def __contains__( self, other ):
        if isinstance( other, Interval ):
            return other.begin >= self.begin and other.end <= self.end
        return other >= self.begin and other <= self.end


    def Overlaps( self, other ):
        return not ( self < other ) and not ( self > other )


    def _SubtractInterval( self, other ):
        if self in other:
            # return invalid interval
            return Interval.Empty()
        i1 = None
        i2 = None
        if other.begin in self:
            i1 = Interval(self.begin, other.begin - 1)
        if other.end in self:
            i2 = Interval(other.end + 1, self.end)

        if i1 and i2:
            return IntervalSet(i1, i2)
        elif i1:
            return i1
        elif i2:
            return i2
        else:
            return self


    def __sub__( self, other ):
        if isinstance( other, Interval ):
            return self._SubtractInterval( other )
        else:
            result = copy.copy( self )
            for i in other:
                result -= i
            return result


    def _union( self, other ):
        if ( self.Precedes( other ) or
             self.Follows( other ) or
             self.Overlaps( other ) ):

            new_begin = min( self.begin, other.begin )
            new_end = max( self.end, other.end )
            return Interval(new_begin, new_end)

        return IntervalSet(self, other)


    __add__ = __or__ = _union


    def __and__( self, other ):
        if isinstance( other, IntervalSet ):
            result = other & self
            l = len( result )
            if l > 1:
                return result
            elif l == 1:
                return result._intervals[ 0 ]
            else:
                return Interval.Empty()
        else:
            if self.Overlaps( other ):
                new_begin = max( self.begin, other.begin )
                new_end = min( self.end, other.end )
                return Interval(new_begin, new_end)
            return Interval.Empty()


    def TopAligns( self, other ):
        return self.begin == other.begin


    def BottomAligns( self, other ):
        return self.end == other.end


    def Follows( self, other ):
        return self.begin == other.end + 1


    def Precedes( self, other ):
        return self.end + 1 == other.begin


    def SingleLine( self ):
        return self.begin == self.end


    def EnlargeTopTo( self, size ):
        l = len( self )
        if l < size:
            self.begin -= size - l
        if self.begin <= 0:
            self.begin = 1
        return self


    def EnlargeBottomTo( self, size ):
        l = len( self )
        if l < size:
            self.end += size - l
        return self


    def LimitBottomBy( self, limit ):
        if self.end > limit:
            self.end = limit
        return self


    def MoveUpBy( self, count ):
        if count >= self.begin:
            count = self.begin - 1
        self.begin -= count
        self.end -= count
        return self


    def MoveDownBy( self, count ):
        self.begin += count
        self.end += count
        return self


    @staticmethod
    def Empty():
        return Interval(0, -1)
