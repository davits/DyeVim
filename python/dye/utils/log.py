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

import logging


def InitLogging( level = None ):

    logging_level = None
    if level == 'info':
        logging_level = logging.INFO
    elif level == 'debug':
        logging_level = logging.DEBUG

    if not logging_level:
        return

    global info, debug
    info = _info
    if logging_level == logging.DEBUG:
        debug = _debug

    logger = logging.getLogger( 'dyevim' )
    logger.setLevel( logging_level )

    fh = logging.FileHandler( 'dyevim.log' )
    fh.setLevel( logging_level )
    logger.addHandler( fh )


def debug( *args ):
    pass


def info( *args ):
    pass


def _get():
    return logging.getLogger( 'dyevim' )


def _debug( *args ):
    _get().debug( *args )


def _info( *args ):
    _get().info( *args )
