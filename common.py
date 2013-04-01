#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, tempfile, shutil
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
		self.__env = _Environment()
		self.platform = sys.platform
		self.arch = self.__env['TARGET_ARCH']
		os.environ['path'] = self.__env['ENV']['PATH']
		self.compiler = ccompiler.get_default_compiler(os.name, sys.platform)
		self.compiler_version = None
		if self.compiler == 'msvc':
			self.compiler_version = self.__env['MSVC_VERSION']


	def configure(self, *args):
		cmd = ['configure']
		if self.platform.startswith('win'):
			cmd[0] = 'configure.bat'

		if args:
			cmd = cmd + list(args)

		subprocess.call(cmd)


	def make(self, *args):
		cmd = ['make']
		if self.platform.startswith('win'):
			if self.compiler == 'msvc':
				cmd[0] = 'nmake'

		if args:
			cmd = cmd + list(args)

		subprocess.call(cmd)

