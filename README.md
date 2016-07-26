DyeVim: semantic highlighting for Vim
=====================================

[![Build Status](https://travis-ci.org/davits/DyeVim.svg?branch=master)](https://travis-ci.org/davits/DyeVim)


This plugin brings semantic highlighting into Vim.

![DyeVim Demo](http://i.imgur.com/3tzV3tP.png)

Semantic tokens are provided by the [ycmd][] and extracted via [YouCompleteMe][] plugin's frontend API. So in order to work DyeVim requires YouCompleteMe plugin to be installed.
DyeVim works out of box and does not require any special configuration (assuming that YouCompleteMe is up and working normal), the only requirement is that it should be added to the Vim's runtimepath after YouCompleteMe.

If you are using Vundle:
    Plugin Valloric/YouCompleteMe
    Plugin davits/DyeVim


Currently required changes are not merged into main repositories yet.
Use this ones if you want to try this out:
https://github.com/davits/ycmd
https://github.com/davits/YouCompleteMe
