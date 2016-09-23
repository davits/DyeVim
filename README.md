DyeVim: semantic highlighting for Vim
=====================================

[![Build Status](https://travis-ci.org/davits/DyeVim.svg?branch=master)](https://travis-ci.org/davits/DyeVim)
[![codecov](https://codecov.io/gh/davits/DyeVim/branch/master/graph/badge.svg)](https://codecov.io/gh/davits/DyeVim)


This plugin brings semantic highlighting into Vim.

![DyeVim Demo](http://i.imgur.com/gDmBwoc.png)

### How it works
Semantic tokens are provided by the [ycmd](https://github.com/Valloric/ycmd) and extracted via [YouCompleteMe](https://github.com/Valloric/YouCompleteMe) plugin's frontend API, so in order to work DyeVim requires YouCompleteMe plugin to be installed.

### Setup
DyeVim works out of box and does not require any special configuration (assuming that YouCompleteMe is up and working normal), the only requirement is that it should be added to the Vim's runtimepath after YouCompleteMe.

Currently required changes are not merged into Valloric/ycmd yet. Use my fork if you want to try this out: https://github.com/davits/YouCompleteMe.

If you are using Vundle:

    Plugin davits/YouCompleteMe
    Plugin davits/DyeVim
