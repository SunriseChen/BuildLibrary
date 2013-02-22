#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, tempfile, shutil
from distutils import util, ccompiler
from SCons.Environment import Environment as _Environment


def modify_file(filename, modify_list):
	text = ''
	with open(filename) as f:
		text = f.read()

	for m in modify_list or []:
		if m[1] not in text:
			text = m[0].sub(m[1], text)

	f = tempfile.NamedTemporaryFile('a', delete=False)
	f.write(text)
	f.close()

	shutil.move(f.name, filename)

class Environment(object):
	def __init__(self):
		env = _Environment()
		self.arch = env['TARGET_ARCH']
		self.platform = sys.platform
		self.compiler = ccompiler.get_default_compiler(os.name, sys.platform)
		self.compiler_version = None
		if self.compiler == 'msvc':
			self.compiler_version = env['MSVC_VERSION']
