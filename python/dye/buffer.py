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


from token import Token
from viewport import Viewport

import bisect
import vim

class Buffer(object):

    def __init__(self):
        self._tokens = []
        self._viewport = Viewport(0, 0)


    def _GetTokensRangeForViewport(self, view):
        if view.IsNull():
            return (0, 0)
        i = bisect.bisect_left(self._tokens, view.begin)
        j = bisect.bisect_right(self._tokens, view.end)
        return (i, j)


    def _CreateMatchesForViewport(self, view):
        token_range = self._GetTokensRangeForViewport(view)
        for i in range(token_range[0], token_range[1]):
            self._tokens[i].AddMatch()

    def _RemoveMatchesFromViewport(self, view):
        token_range = self._GetTokensRangeForViewport(view)
        for i in range(token_range[0], token_range[1]):
            self._tokens[i].RemoveMatch()


    def OnCursorMoved(self):
        current = Viewport.Current()
        if self._viewport != current:
            self.OnViewportChanged(current)


    def OnViewportChanged(self, viewport):
        remove_views = self._viewport - viewport
        for view in remove_views:
            self._RemoveMatchesFromViewport(view)

        apply_views = viewport - self._viewport
        for view in apply_views:
            self._CreateMatchesForViewport(view)

        self._viewport = viewport


    def OnUpdateTokens(self, tokens):
        self._RemoveMatchesFromViewport(self._viewport)
        self._tokens = [Token(t) for t in tokens]
        self._CreateMatchesForViewport(self._viewport)


    def OnLineInserted(self, line, count):
        self._RemoveMatchesFromViewport(Viewport(line, self._viewport.end))

        line_index = bisect.bisect_left(self._tokens, line)
        for i in range(line_index, len(self._tokens)):
            self._tokens[i].line += count

        self._CreateMatchesForViewport(Viewport(line + count, self._viewport.end))


    def OnLineRemoved(self, line, count):
        self._RemoveMatchesFromViewport(Viewport(line, self._viewport.end))

        end = line + count - 1
        token_range = self._GetTokensRangeForViewport(Viewport(line, end))
        del self._tokens[token_range[0] : token_range[1]]

        end_index = bisect.bisect_right(self._tokens, end)
        for i in range(end_index, len(self._tokens)):
            self._tokens[i].line -= count

        self._CreateMatchesForViewport(Viewport(line, self._viewport.end))

