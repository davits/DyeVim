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

import vim

# Interface for closed [b, e] range
class Viewport(object):

    def __init__(self, b, e):
        self.begin = b
        self.end = e


    def __str__(self):
        return '[{0}, {1}]'.format(self.begin, self.end)


    def __eq__(self, other):
        return self.begin == other.begin and self.end == other.end


    def __ne__(self, other):
        return self.begin != other.begin or self.end != other.end


    def __sub__(self, other):

        if other.begin <= self.begin and other.end >= self.end:
            return []

        result = []
        if self._InRange(other.begin):
            r = Viewport(self.begin, other.begin - 1)
            if not r.IsNull():
                result.append(r)

        if self._InRange(other.end):
            r = Viewport(other.end + 1, self.end)
            if not r.IsNull():
                result.append(r)

        if not result:
            result.append(self)

        return result


    def IsNull(self):
        return self.begin > self.end


    def _InRange(self, value):
        return value >= self.begin and value <= self.end


    def Size(self):
        return 0 if self.IsNull() else self.end - self.begin + 1


    @staticmethod
    def Current():
        begin = int(vim.eval('line("w0")'))
        end = int(vim.eval('line("w$")'))
        return Viewport(begin, end)
