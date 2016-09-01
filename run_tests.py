#!/usr/bin/env python

import subprocess
from os import path

DIR_OF_THIS_SCRIPT = path.dirname( path.abspath( __file__ ) )
PYTHON_DIR = path.join( DIR_OF_THIS_SCRIPT, 'python' )


def RunFlake8():
  print( 'Running flake8' )
  subprocess.check_call( [
    'flake8',
    '--select=F,C9',
    '--max-complexity=10',
    PYTHON_DIR
  ] )


def NoseTests():
  subprocess.check_call( [
    'nosetests',
    '--with-coverage',
    '--cover-html',
    '--cover-erase',
    '-v',
    '-w',
    PYTHON_DIR
  ] )


def Main():
  RunFlake8()
  NoseTests()

if __name__ == "__main__":
  Main()
