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

DV_UNIQUE_WID_VAR = 'DyeVimUniqueWId'

class DyeVim( object ):
    def __init__( self, ycm ):
        log.InitLogging()
        self._ycm = ycm
        ycm.RegisterFileParseReadyCallback( self.OnSemanticTokensReady )
        self._buffers = Dict( lambda bufnr: Buffer( bufnr, self._ycm ) )
        self._initialized_filetypes = []
        self._uniqueWId = 1
        self._enteringWindow = False
        self._leavingWindow = 1
        self._leavingBuffer = 1


    def OnSemanticTokensReady( self, bufnr ):
        if vim.current.buffer.number != bufnr:
            return

        log.info( 'OnSemanticTokensReady {0}'.format( bufnr ) )
        self._buffers[ bufnr ].OnUpdateTokens()


    def OnCursorMoved( self ):
        self._buffers[ vim.current.buffer.number ].OnCursorMoved()


    def OnBufferEnter( self ):
        self.InitializeCurrentFiletypeIfNeeded()
        log.info( 'OnBufferEnter %d', vim.current.buffer.number )
        if not self._enteringWindow:
            self._buffers[ self._leavingBuffer ].RemoveMatches()
        self._enteringWindow = False
        self._buffers[ vim.current.buffer.number ].OnEnter()

        # If new buffer is opened in the same window
        # remove matches for old buffer.
        #if self._GetCurrentWId() == self._leavingWindow:
        #    self._buffers[ self._leavingBuffer ].RemoveMatches()
        #self._buffers[ vim.current.buffer.number ].OnEnter()


    def OnBufWinEnter( self ):
        pass


    def OnBufferLeave( self ):
        log.info( 'OnBufferLeave %d', vim.current.buffer.number )
        self._leavingBuffer = vim.current.buffer.number
        self._buffers[ self._leavingBuffer ].OnLeave()


    def OnWinEnter( self ):
        log.info( 'OnWinEnter' )
        self._enteringWindow = True
        self._SetCurrentWId()


    def OnWinLeave( self ):
        self._leavingWindow = self._GetCurrentWId()


    def InitializeCurrentFiletypeIfNeeded( self ):
        ft = vim.current.buffer.options[ 'filetype' ]
        if ft not in self._initialized_filetypes:
            try:
                vim.command('call dyevim#ft#' + ft + '#Setup()')
            except:
                pass
            self._initialized_filetypes.append( ft )


    def _GetCurrentWId( self ):
        return vim.current.window.vars[ DV_UNIQUE_WID_VAR ]


    def _SetCurrentWId( self ):
        if not vim.current.window.vars.has_key( DV_UNIQUE_WID_VAR ):
            vim.current.window.vars[ DV_UNIQUE_WID_VAR ] = self._uniqueWId
            self._uniqueWId += 1
