# adata package 
'''
Adata portable frozen event handling enviroment.

https://github.com/txemavs/adata


Installation
------------
In Windows, you can simply download a frozen release and launch adata.exe.

There is no pip install yet.


Build
-----
If you want to fork this:
- create your new python enviroment and activate it
- use pip to install the requires.txt package list
- clone this repository
- launch adata_run.py


If you want to use the cx_freezer to create your own portable enviroment, check and modify build.py to select packages and run:

    <python> build.py build

'''
# Copyright (c) 2018 Txema Vicente Segura
# 
# MIT License
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

from .core import *

__author__ = 'Txema Vicente'
__version__ = '0.0.1'
