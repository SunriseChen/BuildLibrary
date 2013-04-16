#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, tempfile, shutil
from distutils import ccompiler
from distutils.version import StrictVersion
from distutils.errors import *
from pkg_resources import *
from SCons.Environment import Environment as _Environment


def _args_to_list(args):
	lst = []
	if args:
		for arg in args:
			if isinstance(arg, list):
				lst += arg
			else:
				lst.append(arg)

	return lst


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


def clean_files(*args):
	import glob

	for path in _args_to_list(args):
		if glob.has_magic(path):
			clean_files(glob.glob(path))
		elif os.path.isfile(path):
			os.remove(path)
		elif os.path.isdir(path):
			shutil.rmtree(path)


def get_project_name(lib_info_dir, spec):
	for name in os.listdir(lib_info_dir):
		if spec.lower() == name.lower() and os.path.isdir(os.path.join(lib_info_dir, name)):
			return name

	return spec


def get_lib_name(name, version):
	return '%s-%s' % (name, version)


def get_dist(req, env, source, develop_ok):
	for dist in env[req.key]:
		if dist.precedence==DEVELOP_DIST and not develop_ok:
			continue

		if dist in req and (dist.precedence<=SOURCE_DIST or not source):
			return dist

	raise DistutilsError("Can't get %r" % req)


def generate_setup(lib_info_dir, project_name, version, setup_base):
	from string import Template

	src_file = os.path.join(lib_info_dir, project_name, 'setup.py')
	setup_script = os.path.join(setup_base, 'setup.py')
	print('Writing %s' % setup_script)
	with open(setup_script, 'w') as dst:
		with open(src_file) as src:
			for line in src:
				line = Template(line).safe_substitute(
					name=project_name,
					version=version,
					lib_name=get_lib_name(project_name, version),
				)
				dst.write(line)

	return setup_script


def generate_import(base_dir, project_name, version):
	if sys.platform == 'win32':
		import ntfslink

		source = os.path.join(base_dir, project_name,
			get_lib_name(project_name, version))
		import_link = os.path.join(base_dir, 'Import', project_name)

		if os.path.exists(import_link):
			if os.path.isfile(import_link):
				os.remove(import_link)
			elif os.path.islink(import_link):
				os.rmdir(import_link)
			else:
				shutil.rmtree(import_link)
		else:
			ensure_directory(import_link)

		os.symlink(source, import_link)


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
		if self.compiler == 'msvc':
			cmd[0] = 'nmake'

		cmd += _args_to_list(args)

		return subprocess.call(cmd) if cmd else False

