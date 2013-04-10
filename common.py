#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, tempfile, shutil
from distutils import ccompiler
from distutils.version import StrictVersion
from distutils.errors import *
from pkg_resources import *
from SCons.Environment import Environment as _Environment


def modify_file(filename, modify_list):
	if not os.path.isfile(filename):
		return

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
		elif os.path.isfile(path):
			os.remove(path)
		elif os.path.isdir(path):
			shutil.rmtree(path)


def get_lib_name(lib_info_dir, spec):
	for name in os.listdir(lib_info_dir):
		if spec.lower() == name.lower() and os.path.isdir(os.path.join(lib_info_dir, name)):
			return name

	return spec


def get_dist(req, env, source, develop_ok):
	for dist in env[req.key]:
		if dist.precedence==DEVELOP_DIST and not develop_ok:
			continue

		if dist in req and (dist.precedence<=SOURCE_DIST or not source):
			return dist

	raise DistutilsError("Can't get %r" % req)


def generate_setup(dist, lib_info_dir, setup_base, basename):
	from string import Template

	src_file = os.path.join(lib_info_dir, dist.project_name, 'setup.py')
	setup_script = os.path.join(setup_base, 'setup.py')
	print('Writing %s' % setup_script)
	with open(setup_script, 'w') as dst:
		with open(src_file) as src:
			for line in src:
				line = Template(line).safe_substitute(
					version=dist.version,
					basename=basename,
				)
				dst.write(line)

	return setup_script


class Environment(object):
	def __init__(self):
		env = _Environment()
		self.arch = env['TARGET_ARCH']
		self.platform = sys.platform
		self.compiler = ccompiler.get_default_compiler()
		self.compiler_version = StrictVersion('0.0')
		if self.compiler == 'msvc':
			self.compiler_version = StrictVersion(env['MSVC_VERSION'])
			os.environ['PATH'] = env['ENV']['PATH']
			os.environ['INCLUDE'] = env['ENV']['INCLUDE']
			os.environ['LIB'] = env['ENV']['LIB']
			os.environ['LIBPATH'] = env['ENV']['LIBPATH']


	def configure(self, *args):
		cmd = ['./configure']
		if self.platform.startswith('win'):
			cmd[0] = 'configure.bat'
		elif not os.path.exists(cmd[0]):
			cmd[0] = './configure.sh'

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

