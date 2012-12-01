#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

PYTHON_HOME = sys.prefix

# 目录可以使用绝对路径和相对路径（相对当前目录），为 None 则使用临时目录
DOWNLOAD_DIR = None

UNPACK_DIR = None

BUILD_DIR = None

INSTALL_DIR = ''

if os.path.exists('local_settings.py'):
	from local_settings import *

