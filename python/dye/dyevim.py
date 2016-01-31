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


from buffer import Buffer
from dict import Dict
import log

import vim

class DyeVim( object ):
    def __init__( self, ycm ):
        log.InitLogging()
        self._ycm = ycm
        ycm.RegisterFileParseReadyCallback( self.OnSemanticTokensReady )
        self._buffers = Dict( lambda bufnr: Buffer( bufnr, self._ycm ) )
        self._current_buffer = 0
        self._current_window = (0, 0)
        self._initialized_filetypes = []


    def OnSemanticTokensReady( self, bufnr ):
        if vim.current.buffer.number != bufnr:
            return

        log.info( 'OnSemanticTokensReady {0}'.format( bufnr ) )
        self._buffers[ bufnr ].OnUpdateTokens()


    def OnCursorMoved( self ):
        self._buffers[ vim.current.buffer.number ].OnCursorMoved()


    def OnBufferEnter( self ):
        self.InitializeCurrentFiletypeIfNeeded()

        cw = ( vim.current.tabpage.number, vim.current.window.number )
        # If we are opening new buffer in the same (tab, window)
        # then old buffer tokens need to be removed
        if cw == self._current_window:
            self._buffers[ self._current_buffer ].RemoveMatches()
        else:
            self._current_window = cw
        self._current_buffer = vim.current.buffer.number
        self._buffers[ self._current_buffer ].OnEnter()


    def InitializeCurrentFiletypeIfNeeded( self ):
        ft = vim.current.buffer.options[ 'filetype' ]
        if ft not in self._initialized_filetypes:
            try:
                vim.command('call dyevim#ft#' + ft + '#Setup()')
            except:
                pass
            self._initialized_filetypes.append( ft )


    def OnBufferLeave( self ):
        pass
        #self._buffers[ vim.current.buffer.number ].OnLeave()
