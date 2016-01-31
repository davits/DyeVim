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

from nose.tools import eq_, ok_, assert_raises

from dye.interval import Interval
from dye.interval_set import IntervalSet


def Construction_test():
    eq_( IntervalSet( Interval( 1, 10 ), Interval( 20, 30 ) ),
         IntervalSet( Interval( 20, 30 ), Interval( 1, 10 ) ) )


def Contains_test():
    s = IntervalSet( Interval( 1, 10 ), Interval( 20, 30 ), Interval( 40, 50 ) )

    assert_raises( TypeError, IntervalSet.__contains__, s, IntervalSet() )

    ok_( Interval( 1, 10 ) in s )
    ok_( Interval( 25, 27 ) in s )
    ok_( Interval( 40, 48 ) in s )
    ok_( Interval( 8, 11 ) not in s )
    ok_( Interval( 11, 15 ) not in s )
    ok_( Interval( 5, 25 ) not in s )
    ok_( Interval( 25, 45 ) not in s )
    ok_( Interval( 15, 35 ) not in s )
    ok_( Interval( 0, 55 ) not in s )

    ok_( 1 in s )
    ok_( 30 in s )
    ok_( 45 in s )
    ok_( 0 not in s )
    ok_( 11 not in s )
    ok_( 35 not in s )
    ok_( 39 not in s )
    ok_( 55 not in s )


def Union_test():
    s = IntervalSet()

    s |= Interval( 1, 10 )
    eq_( s, IntervalSet( Interval( 1, 10 ) ) )

    s |= Interval( 20, 30 )
    eq_( s, IntervalSet( Interval( 1, 10 ), Interval( 20, 30 ) ) )

    s |= Interval( 40, 50 )
    eq_( s, IntervalSet( Interval( 1, 10 ), Interval( 20, 30 ),
                         Interval( 40, 50 ) ) )

    eq_( s | Interval( 11, 19 ), IntervalSet( Interval( 1, 30 ),
                                              Interval( 40, 50 ) ) )

    eq_( s | Interval( 11, 15 ), IntervalSet( Interval( 1, 15 ),
                                              Interval( 20, 30 ),
                                              Interval( 40, 50 ) ) )

    eq_( s | Interval( 32, 39 ), IntervalSet( Interval( 1, 10 ),
                                              Interval( 20, 30 ),
                                              Interval( 32, 50 ) ) )

    eq_( s | Interval( 32, 38 ), IntervalSet( Interval( 1, 10 ),
                                              Interval( 20, 30 ),
                                              Interval( 32, 38 ),
                                              Interval( 40, 50 ) ) )

    eq_( s | IntervalSet( Interval( 11, 19 ), Interval( 35, 39 ) ),
         IntervalSet( Interval( 1, 30 ), Interval( 35, 50 ) ) )


def Intersect_test():
    s = IntervalSet( Interval( 1, 10 ), Interval( 20, 30 ), Interval( 40, 50 ) )

    eq_( s & Interval( 11, 19 ), IntervalSet() )
    eq_( s & Interval( 5, 15 ), IntervalSet( Interval( 5, 10 ) ) )

    eq_( s & Interval( 5, 25 ), IntervalSet( Interval( 5, 10 ),
                                             Interval( 20, 25 ) ) )
    eq_( s & Interval( 0, 51 ), s )


def Subtract_test():
    s = IntervalSet( Interval( 1, 10 ), Interval( 20, 30 ), Interval( 40, 50 ) )

    eq_( s - Interval( 1, 50 ), IntervalSet() )
    eq_( s - Interval( 1, 9 ), IntervalSet( Interval( 10, 10 ),
                                            Interval( 20, 30 ),
                                            Interval( 40, 50 ) ) )

    eq_( s - Interval( 25, 25 ), IntervalSet( Interval( 1, 10 ),
                                              Interval( 20, 24 ),
                                              Interval( 26, 30 ),
                                              Interval( 40, 50 ) ) )


def BestQueryRange_test():
    s = IntervalSet()
    r = s.GetIntervalForQuery( Interval( 30, 40 ), 10 )
    eq_( r, Interval( 30, 40 ) )
    s |= r # [ [30, 40] ]

    r = s.GetIntervalForQuery( Interval( 29, 29 ), 10 )
    eq_( r, Interval( 20, 29 ) )
    s |= r # [ [20, 40] ]

    r = s.GetIntervalForQuery( Interval( 31, 41 ), 10 )
    eq_( r, Interval( 41, 50 ) )
    s |= r # [ [20, 50] ]

    r = s.GetIntervalForQuery( Interval( 60, 60 ), 10 )
    eq_( r, Interval( 60, 69 ) )
    s |= r # [ [20, 50], [60, 69] ]

    r = s.GetIntervalForQuery( Interval( 59, 68 ), 10 )
    eq_( r, Interval( 51, 59 ) )
    s |= r # [ [20, 69] ]

    r = s.GetIntervalForQuery( Interval( 85, 100 ), 10 )
    eq_( r, Interval( 85, 100 ) )
    s |= r # [ [20, 69], [85, 100] ]

    r = s.GetIntervalForQuery( Interval( 61, 70 ), 10 )
    eq_( r, Interval( 70, 79 ) )
    # [ [20, 69], [85, 100] ]

    r = s.GetIntervalForQuery( Interval( 83, 92 ), 10 )
    eq_( r, Interval( 75, 84 ) )
    # [ [20, 69], [85, 100] ]

    r = s.GetIntervalForQuery( Interval( 72, 81 ), 10 )
    eq_( r, Interval( 72, 81 ) )
    s |= r # [ [20, 69], [72, 81], [85, 100] ]

    r = s.GetIntervalForQuery( Interval( 69, 85 ), 10 )
    eq_( r, IntervalSet( Interval( 70, 71 ), Interval( 82, 84 ) ) )
    s |= r # [20, 100]

    eq_( s, IntervalSet( Interval( 20, 100 ) ) )

    s = IntervalSet()
    r = s.GetIntervalForQuery( Interval( 9, 9 ), 20 )
    eq_( r, Interval( 9, 28 ) )
    s |= r # [9, 28]

    r = s.GetIntervalForQuery( Interval( 8, 8 ), 20 )
    eq_( r, Interval( 1, 8 ) )
    s |= r # [1, 28]

    eq_( s, IntervalSet( Interval( 1, 28 ) ) )
