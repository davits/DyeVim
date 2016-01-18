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

from range import Range

from bisect import bisect_left, bisect_right


class TokenProvider(object):

    def __init__(self, bufnr):
        self._bufnr = bufnr
        self._tokens = []
        self._ranges = []


    def UpdateTokens(self, lr):
        self._tokens = []
        self._ranges = []


    def GetTokens(self, query_range):
        # extend query_range to the viewport size
        l = bisect_left(self._ranges, query_range)
        r = bisect_right(self._ranges, query_range)
        if l == r:
            self._QueryTokensAndStore(query_range)


    def _QueryTokens(self, lr):
        tokens = self._extractor.GetSemanticTokens(lr.begin, lr.end)
