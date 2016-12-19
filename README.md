DyeVim: C++ semantic highlighting for Vim
=========================================

[![Build Status](https://travis-ci.org/davits/DyeVim.svg?branch=master)](https://travis-ci.org/davits/DyeVim)
[![codecov](https://codecov.io/gh/davits/DyeVim/branch/master/graph/badge.svg)](https://codecov.io/gh/davits/DyeVim)


This plugin brings semantic highlighting into Vim.
Once you have seen your code in color you will never go back to black&white.

Pictures worth a thousand words:
![DyeVim Demo](http://i.imgur.com/ASQnHS0.png?1)
![DyeVim Demo Token](http://i.imgur.com/kGhMXab.png?1)

### Possibilities
Currently it can differentiate and higlight the following C++ idioms:

    Namespace
    Class, Struct, Union, TypeAlias
    Variable, GlobalVariable, MemberVariable, StaticMemberVariable
    Function, MemberFunction, StaticMemberFunction
    FunctionParameter
    Enumeration, Enumerator
    TemplateParameter, TemplateNonTypeParameter
    Macro, PreprocessingDirective

It also greys out the skipped ranges between #ifdef...#endif preprocessing directives.
![Skipped Ranges](http://i.imgur.com/049354Y.png?1)

### How it works
Semantic tokens are provided by the [clang](http://clang.llvm.org/), extracted by the [ycmd](https://github.com/davits/ycmd) and obtained via [YouCompleteMe](https://github.com/davits/YouCompleteMe) plugin's frontend API, so in order to work DyeVim requires YouCompleteMe plugin to be installed.

Currently I am maintaining my own forks for [ycmd](https://github.com/davits/ycmd) and [YouCompleteMe](https://github.com/davits/YouCompleteMe) with changes required for the semantic tokens to work, but I hope that in time these changes will be merged back.

### Setup
DyeVim works out of box and does not require any special configuration (assuming that YouCompleteMe is up and working normal), the only requirement is that it should be added to the Vim's runtimepath after YouCompleteMe.

If you are using Vundle:

    Plugin davits/YouCompleteMe
    Plugin davits/DyeVim

Currently only 2 colorschemes are supported: wombat256mod and solarized.
If your colorscheme is not supported DyeVim will try its best to highlight your code by adding bold and italic modifiers to the existing colors.

You can also place your own coloring scheme in the autoload/dyevim/ft/cpp directory named your_colorscheme.vim (see existing ones as an example).

### Caveats
C highlighting is not working yet, but it will be soon (need to add coloring scheme).

Since I mainly use gvim in my workflow, there is no terminal support... yet, sorry for that.


### Acknowledgements
Thanks to the [YouCompleteMe](https://github.com/Valloric/YouCompleteMe) maintainers team for the inspiration, help and support.

I walked the path prepared by the [color_coded](https://github.com/jeaye/color_coded) plugin.
