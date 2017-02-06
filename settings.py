#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
全局通用配置文件。本地特定配置文件使用“local_settings.py”文件。
'''

# pylint: disable=C0325,E0401,W0401

import os
import sys

PYTHON_HOME = sys.prefix

# 目录可以使用绝对路径和相对路径（相对当前目录），为 None 则使用临时目录
DOWNLOAD_DIR = None
UNPACK_DIR = None
BUILD_DIR = None
INSTALL_DIR = ''

if os.path.exists('local_settings.py'):
    from local_settings import *


def test():
    '''测试'''
    print('PYTHON_HOME = "%s"' % PYTHON_HOME)
    print('DOWNLOAD_DIR = "%s"' % DOWNLOAD_DIR)
    print('UNPACK_DIR = "%s"' % UNPACK_DIR)
    print('BUILD_DIR = "%s"' % BUILD_DIR)
    print('INSTALL_DIR = "%s"' % INSTALL_DIR)
    print('Test passed !')


if __name__ == '__main__':
    test()
