#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

PYTHON_HOME = sys.prefix

# Ŀ¼����ʹ�þ���·�������·������Ե�ǰĿ¼����Ϊ None ��ʹ����ʱĿ¼
DOWNLOAD_DIR = None

UNPACK_DIR = None

BUILD_DIR = None

INSTALL_DIR = ''

if os.path.exists('local_settings.py'):
	from local_settings import *

