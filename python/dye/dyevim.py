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

from .buffer import Buffer
from .window import Window
from .dict import Dict
from . import log

from collections import defaultdict

import vim

DV_UNIQUE_WID_VAR = 'DyeVimUniqueWId'

class DyeVim( object ):
    def __init__( self, ycm ):
        log.InitLogging('debug')
        ycm.RegisterFileParseReadyCallback( self.OnSemanticTokensReady )
        self._ycm = ycm
        self._buffers = Dict( lambda bufnr: Buffer( bufnr, self._ycm ) )
        self._windows = Dict( lambda wid: Window( wid,
                                                  self._GetWIdBuffer( wid ) ) )
        self._windowBuffer = defaultdict( int )
        self._initialized_filetypes = set()
        self._nextUniqueWId = 1
        self._enteringWindow = False


    def OnSemanticTokensReady( self, bufnr ):
        log.info( 'OnSemanticTokensReady buffer: {0}'.format( bufnr ) )
        if vim.current.buffer.number != bufnr:
            return
        self._windows[ self._GetCurrentWId() ].OnUpdateTokens()


    def OnCursorMoved( self ):
        self._windows[ self._GetCurrentWId() ].OnCursorMoved()


    def OnWindowEnter( self ):
        self._SetCurrentWId()


    def OnBufferEnter( self ):
        self.InitializeCurrentFiletypeIfNeeded()
        wid = self._GetCurrentWId()
        bnr = vim.current.buffer.number
        if self._windowBuffer[ wid ] != bnr:
            self._windowBuffer[ wid ] = bnr
            self._windows[ wid ].OnBufferChanged( self._buffers[ bnr ] )


    def InitializeCurrentFiletypeIfNeeded( self ):
        ft = vim.current.buffer.options[ 'filetype' ]
        if ft not in self._initialized_filetypes:
            try:
                vim.command('call dyevim#ft#' + ft + '#Setup()')
            except:
                pass
            self._initialized_filetypes.add( ft )


    def _GetCurrentWId( self ):
        return vim.current.window.vars[ DV_UNIQUE_WID_VAR ]


    def _SetCurrentWId( self ):
        if not vim.current.window.vars.has_key( DV_UNIQUE_WID_VAR ):
            vim.current.window.vars[ DV_UNIQUE_WID_VAR ] = self._nextUniqueWId
            self._nextUniqueWId += 1


    def _GetWIdBuffer( self, wid ):
        return self._buffers[ self._windowBuffer[ wid ] ]
