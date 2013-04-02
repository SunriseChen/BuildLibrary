#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, tempfile, shutil
from distutils import ccompiler
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


def _args_to_list(args):
	lst = []
	if args:
		for a in args:
			if isinstance(a, list):
				lst += a
			else:
				lst.append(a)

	return lst


def clean_files(*args):
	import glob

	for path in _args_to_list(args):
		if glob.has_magic(path):
			clean_files(glob.glob(path))
		elif os.path.exists(path):
			if os.path.isfile(path):
				os.remove(path)
			elif os.path.isdir(path):
				shutil.rmtree(path)


class Environment(object):
	def __init__(self):
		env = _Environment()
		self.platform = sys.platform
		self.arch = env['TARGET_ARCH']
		os.environ['PATH'] = env['ENV']['PATH']
		os.environ['INCLUDE'] = env['ENV']['INCLUDE']
		os.environ['LIB'] = env['ENV']['LIB']
		os.environ['LIBPATH'] = env['ENV']['LIBPATH']
		self.compiler = ccompiler.get_default_compiler()
		self.compiler_version = None
		if self.compiler == 'msvc':
			self.compiler_version = env['MSVC_VERSION']


	def configure(self, *args):
		cmd = ['configure']
		if self.platform.startswith('win'):
			cmd[0] = 'configure.bat'
		elif not os.path.exists(cmd[0]):
			cmd[0] = 'configure.sh'

		if os.path.exists(cmd[0]):
			cmd += _args_to_list(args)
		else:
			cmd = _args_to_list(args)

		return subprocess.call(cmd) if cmd else False


	def make(self, *args):
		cmd = ['make']
		if self.platform.startswith('win'):
			if self.compiler == 'msvc':
				cmd[0] = 'nmake'

		cmd += _args_to_list(args)

		return subprocess.call(cmd) if cmd else False

