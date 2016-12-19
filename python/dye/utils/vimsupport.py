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

import vim


def GetCurrentBufferNumber():
    return vim.current.buffer.number


def BufNumberToName( bufnr ):
    return vim.eval( 'bufname({0})'.format( bufnr ) )


def GetCurrentTopLine():
    return int( vim.eval( 'line("w0")' ) )


def GetCurrentBottomLine():
    return int( vim.eval( 'line("w$")' ) )


def GetCurrentWindowHeight():
    return int( vim.current.window.height )


def GetFileType( bufnr ):
    return vim.buffers[ bufnr ].options[ 'filetype' ]


def GetBufferLen( bufnr ):
    return len( vim.buffers[ bufnr ] )


def GetLineLen( bufnr, line ):
    # line index is 1 based, but vim python interface is 0 based
    return len( vim.buffers[ bufnr ][ line - 1 ] )


def GetIntValue( name ):
    return int( vim.eval( name ) )


def PostVimWarning( message ):
    # Displaying a new message while previous ones are still on the status line
    # might lead to a hit-enter prompt or the message appearing without a
    # newline so we do a redraw first.
    vim.command( 'redraw' )
    vim.command( 'echohl WarningMsg' )
    vim.command( "echom '{0}'".format( message ) )
    vim.command( 'echohl None' )
