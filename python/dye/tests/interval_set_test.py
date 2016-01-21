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

    #ok_( 1 in s )
    #ok_( 30 in s )
    #ok_( 45 in s )
    #ok_( 0 not in s )
    #ok_( 11 not in s )
    #ok_( 35 not in s )
    #ok_( 39 not in s )
    #ok_( 55 not in s )
