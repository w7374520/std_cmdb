#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

#设置工作目录，使得包和模块能够正常导入
BASE_DIR = os.path.dirname(os.getcwd())
sys.path.append(BASE_DIR)

from core import handler

if __name__ == '__main__':
    handler.ArgvHandler(sys.argv)

