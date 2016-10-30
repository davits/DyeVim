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

from dye.interval.interval import Interval
from dye.interval.interval_set import IntervalSet

from nose.tools import eq_, ok_


def String_test():
    # 100% coverage baby
    eq_( "%s" % Interval( 1, 10 ), "[1, 10]" )

def Boolean_test():
    ok_( Interval( 1, 1 ) )
    ok_( Interval( 1, 10 ) )
    ok_( not Interval( 2, 1 ) )
    ok_( not Interval( 0, 0 ) )
    ok_( not Interval( 0, 5 ) )
    ok_( not Interval( -1, 1 ) )
    ok_( not Interval.Empty() )


def Length_test():
    eq_( len( Interval( 1, 1 ) ), 1 )
    eq_( len( Interval( 1, 10 ) ), 10 )
    eq_( len( Interval( 10, 20 ) ), 11 )
    eq_( len( Interval( 0, 1 ) ), 2)


def Comparison_test():
    eq_( Interval( 1, 10 ), Interval( 1, 10 ) )

    ok_( Interval( 1, 10 ) != Interval( 1, 11 ) )
    ok_( Interval( 1, 10 ) != Interval( 2, 10 ) )
    ok_( Interval( 1, 10 ) != Interval( 2, 11 ) )

    ok_( Interval( 1, 10 ) < Interval( 11, 20 ) )
    ok_( not ( Interval( 1, 10 ) < Interval( 10, 20 ) ) )
    ok_( not ( Interval( 1, 10 ) < Interval( 5, 20 ) ) )
    ok_( not ( Interval( 1, 10 ) < Interval( 2, 9 ) ) )

    ok_( Interval( 11, 20 ) > Interval( 1, 10 ) )
    ok_( not ( Interval( 10, 20 ) > Interval( 1, 10 ) ) )
    ok_( not ( Interval( 10, 20 ) > Interval( 1, 15 ) ) )
    ok_( not ( Interval( 10, 20 ) > Interval( 12, 19 ) ) )


def Contains_test():
    ok_( 1 in Interval( 1, 10 ) )
    ok_( 10 in Interval( 1, 10 ) )
    ok_( 5 in Interval( 1, 10 ) )
    ok_( 0 not in Interval( 1, 10 ) )
    ok_( 11 not in Interval( 1, 10 ) )

    ok_( Interval( 10, 20 ) in Interval( 10, 20 ) )
    ok_( Interval( 12, 20 ) in Interval( 10, 20 ) )
    ok_( Interval( 10, 18 ) in Interval( 10, 20 ) )
    ok_( Interval( 12, 18 ) in Interval( 10, 20 ) )
    ok_( Interval( 1, 9 ) not in Interval( 10, 20 ) )
    ok_( Interval( 1, 10 ) not in Interval( 10, 20 ) )
    ok_( Interval( 9, 15 ) not in Interval( 10, 20 ) )
    ok_( Interval( 21, 30 ) not in Interval( 10, 20 ) )
    ok_( Interval( 20, 30 ) not in Interval( 10, 20 ) )
    ok_( Interval( 15, 21 ) not in Interval( 10, 20 ) )
    ok_( Interval( 5, 25 ) not in Interval( 10, 20 ) )


def Operlap_test():
    ok_( Interval( 10, 20 ).Overlaps( Interval( 10, 20 ) ) )
    ok_( Interval( 10, 20 ).Overlaps( Interval( 1, 10 ) ) )
    ok_( Interval( 10, 20 ).Overlaps( Interval( 1, 15 ) ) )
    ok_( Interval( 10, 20 ).Overlaps( Interval( 20, 30 ) ) )
    ok_( Interval( 10, 20 ).Overlaps( Interval( 17, 30 ) ) )
    ok_( Interval( 10, 20 ).Overlaps( Interval( 12, 18 ) ) )
    ok_( Interval( 10, 20 ).Overlaps( Interval( 5, 25 ) ) )


def Subtract_test():
    ok_( not ( Interval( 10, 20 ) - Interval( 10, 20 ) ) )
    ok_( not ( Interval( 10, 20 ) - Interval( 5, 25 ) ) )
    eq_( Interval( 10, 20 ) - Interval( 10, 20 ), Interval.Empty() )
    eq_( Interval( 10, 20 ) - Interval( 5, 25 ), Interval.Empty() )
    eq_( Interval( 10, 20 ) - Interval( 1, 10 ), Interval( 11, 20 ) )
    eq_( Interval( 10, 20 ) - Interval( 1, 13 ), Interval( 14, 20 ) )
    eq_( Interval( 10, 20 ) - Interval( 20, 30 ), Interval( 10, 19 ) )
    eq_( Interval( 10, 20 ) - Interval( 16, 30 ), Interval( 10, 15 ) )
    eq_( Interval( 10, 20 ) - Interval( 14, 17 ),
         IntervalSet( Interval( 10, 13 ), Interval( 18, 20 ) ) )

    eq_( Interval( 1, 10 ) - IntervalSet( Interval( 2, 3 ), Interval( 5, 7 ) ),
         IntervalSet( Interval( 1, 1 ), Interval( 4, 4 ), Interval( 8, 10 ) ) )


def Union_test():
    eq_( Interval( 1, 10 ) | Interval( 11, 20 ), Interval( 1, 20 ) )
    eq_( Interval( 20, 30 ) | Interval( 10, 19 ), Interval( 10, 30 ) )
    eq_( Interval( 1, 10 ) | Interval( 8, 20 ), Interval( 1, 20 ) )
    eq_( Interval( 1, 10 ) | Interval( 15, 20 ),
         IntervalSet( Interval( 1, 10 ), Interval( 15, 20 ) ) )
    eq_( Interval( 15, 20 ) | Interval( 1, 10 ),
         IntervalSet( Interval( 1, 10 ), Interval( 15, 20 ) ) )


def Intersect_test():
    eq_( Interval( 10, 20 ) & Interval( 1, 9 ), Interval.Empty() )
    eq_( Interval( 10, 20 ) & Interval( 21, 30 ), Interval.Empty() )
    eq_( Interval( 10, 20 ) & Interval( 20, 30 ), Interval( 20, 20 ) )
    eq_( Interval( 10, 20 ) & Interval( 1, 10 ), Interval( 10, 10 ) )
    eq_( Interval( 10, 20 ) & Interval( 1, 15 ), Interval( 10, 15 ) )
    eq_( Interval( 10, 20 ) & Interval( 17, 25 ), Interval( 17, 20 ) )
    eq_( Interval( 10, 20 ) & Interval( 1, 30 ), Interval( 10, 20 ) )

    s = IntervalSet( Interval( 5, 10 ), Interval( 20, 25 ) )
    eq_( Interval( 1, 4 ) & s, Interval.Empty() )
    eq_( Interval( 7, 15 ) & s, Interval( 7, 10 ) )
    eq_( Interval( 23, 30 ) & s, Interval( 23, 25 ) )
    eq_( Interval( 26, 30 ) & s, Interval.Empty() )
    eq_( Interval( 7, 25 ) & s,
         IntervalSet( Interval( 7, 10 ), Interval( 20, 25 ) ) )


def Operations_test():
    eq_( Interval( 5, 10 ).EnlargeTopTo( 10 ), Interval( 1, 10 ) )
    eq_( Interval( 5, 10 ).EnlargeTopTo( 11 ), Interval( 1, 10 ) )
    eq_( Interval( 10, 20 ).EnlargeTopTo( 15 ), Interval( 6, 20 ) )

    eq_( Interval( 1, 10 ).EnlargeBottomTo( 20 ), Interval( 1, 20 ) )

    eq_( Interval( 10, 20 ).MoveUpBy( 5 ), Interval( 5, 15 ) )
    eq_( Interval( 11, 20 ).MoveUpBy( 10 ), Interval( 1, 10 ) )
    eq_( Interval( 2, 10 ).MoveUpBy( 5 ), Interval( 1, 9 ) )

    eq_( Interval( 1, 10 ).MoveDownBy( 10 ), Interval( 11, 20 ) )

    eq_( Interval( 1, 5 ).LimitBottomBy( 10 ), Interval( 1, 5 ) )
    eq_( Interval( 1, 5 ).LimitBottomBy( 5 ), Interval( 1, 5 ) )
    eq_( Interval( 1, 10 ).LimitBottomBy( 5 ), Interval( 1, 5 ) )


# I'm new to python
def Reference_test():
    i1 = Interval( 1, 10 )
    i1c = Interval( 1, 10 )
    i2 = Interval( 5, 15 )
    i2c = Interval( 5, 15 )

    i3 = i1 - i2
    eq_( i1, i1c )
    eq_( i2, i2c )

    i3 = i1 | i2
    eq_( i1, i1c )
    eq_( i2, i2c )

    i3 = i1 & i2
    eq_( i1, i1c )
    eq_( i2, i2c )

    eq_( i3, Interval( 5, 10 ) )
