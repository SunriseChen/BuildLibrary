#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

DEFAULT_VERSION = ""
DEFAULT_URL     = ""

md5_data = {
		}

try:
	# Python version >= 2.5
	from hashlib import md5
except ImportError:
	# Python version < 2.5
	from md5 import md5

def validate_md5(lib_name, data, lib_digest = md5_data):
	if lib_name in lib_digest:
		digest = md5(data).hexdigest()
		if digest != lib_digest[lib_name]:
			print('')
			sys.exit(2)
	return data

#git clone https://github.com/SunriseChen/BuildLibrary.git
