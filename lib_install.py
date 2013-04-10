#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, tempfile, shutil

DEFAULT_VERSION = '0.1.0'
DEFAULT_URL     = 'https://github.com/SunriseChen/BuildLibrary/archive/master.zip'
PACK_FILE_ROOT_DIR = 'BuildLibrary-master'

SETUPTOOLS_URL = 'http://python-distribute.org/distribute_setup.py'
LIB_INFO_DIR = 'lib_info'

TEMP_DIR_PREFIX = 'lib_install-'
PTH_FILE_NAME = 'lib-install.pth'


def download_file(url, target_dir=os.curdir):
	import urllib2

	print('Downloading %s' % url)
	remote_file = urllib2.urlopen(url)

	if not os.path.exists(target_dir):
		os.makedirs(target_dir)
	file_name = os.path.basename(url)
	file_path = os.path.join(target_dir, file_name)
	with open(file_path, 'wb') as local_file:
		local_file.write(remote_file.read())

	remote_file.close()
	print('Downloaded.')

	return os.path.realpath(file_path)


def restart():
	subprocess.call(['python'] + sys.argv)
	sys.exit()


def install_setuptools():
	print('Install setuptools...')
	setuptools = download_file(SETUPTOOLS_URL)
	if subprocess.call(['python', setuptools]) == 0:
		restart()


def check_setuptools(times=3):
	for i in range(times):
		try:
			import setuptools
			break
		except ImportError:
			install_setuptools()
	else:
		print('Install setuptools fail!')
		sys.exit(1)


def install_scons():
	print('Install SCons...')
	cmd = ['easy_install', 'SCons']
	if not sys.platform.startswith('win'):
		cmd[0] = os.path.join('/usr/bin', cmd[0])
	subprocess.call(cmd)


def check_scons(times=3):
	import re

	for i in range(times):
		try:
			import pkg_resources
			d = pkg_resources.get_distribution('scons')
			path = '%s/scons-%s' % (d.location, d.version)
			sys.path.insert(0, path)
			import SCons
			break
		except (pkg_resources.DistributionNotFound, ImportError):
			install_scons()
	else:
		print('Install SCons fail!')
		sys.exit(1)


def move_files(src_dir, dst_dir, ignore=None):
	names = os.listdir(src_dir)
	if ignore:
		ignored_names = ignore(src_dir, names)
	else:
		ignored_names = set()

	if not os.path.exists(dst_dir):
		os.makedirs(dst_dir)
	for name in names:
		if name in ignored_names:
			continue
		src_name = os.path.join(src_dir, name)
		dst_name = os.path.join(dst_dir, name)
		if os.path.islink(src_name):
			if os.path.isfile(dst_name):
				os.remove(dst_name)
			elif os.path.isdir(dst_name):
				shutil.rmtree(dst_name)
			linkto = os.readlink(src_name)
			os.symlink(linkto, dst_name)
		elif os.path.isdir(src_name):
			if os.path.isfile(dst_name) or os.path.islink(dst_name):
				os.remove(dst_name)
			move_files(src_name, dst_name, ignore)
		else:
			if os.path.islink(dst_name):
				os.remove(dst_name)
			elif os.path.isdir(dst_name):
				shutil.rmtree(dst_name)
			shutil.move(src_name, dst_name)


def update_self():
	if len(sys.argv) > 1 and sys.argv[1] == '--updated':
		del sys.argv[1]
		return

	from setuptools.package_index import PackageIndex
	from setuptools.archive_util import unpack_archive

	tmpdir = tempfile.mkdtemp(prefix=TEMP_DIR_PREFIX)
	print('Downloading %s' % DEFAULT_URL)
	download = PackageIndex().download(DEFAULT_URL, tmpdir)
	print('Downloaded.')
	unpack_archive(download, tmpdir)
	unpack_dir = os.path.join(tmpdir, PACK_FILE_ROOT_DIR)
	move_files(unpack_dir, os.curdir,
		shutil.ignore_patterns('.*', '*.sln', '*.pyproj', '*.sample'))
	shutil.rmtree(tmpdir)
	print('Self updated.')

	if len(sys.argv) == 1:
		# only update self.
		sys.exit()
	else:
		sys.argv.insert(1, '--updated')
		restart()


def check_env():
	check_setuptools()
	check_scons()
	update_self()


def show_sys_vars():
	print('os.name = %s, sys.platform = %s' % (os.name, sys.platform))

	from distutils import util, ccompiler
	print('platform = %s' % util.get_platform())
	print('compiler = %s' % ccompiler.get_default_compiler())

	from SCons.Environment import Environment
	env = Environment()
	vars = [
		'CC',
		'CXX',
		'PLATFORM',
		'MSVC_VERSION',
		'TARGET',
		'TARGET_ARCH',
		'TARGET_OS',
		'MSVS',
		'MSVS_VERSION',
		'MSVS_ARCH',
		'TOOLS',
		'HOST_ARCH',
		'HOST_OS',
		'MSVC_BATCH',
		'MSVC_USE_SCRIPT',
	]
	for var in vars:
		print('%s = %r' % (var, env.subst('$' + var)))


check_env()
#show_sys_vars()
#exit()


from distutils import log
from setuptools.command.easy_install import *
from setuptools.command.easy_install import rmtree
from pkg_resources import *
#from distutils.errors import *
from common import *


class lib_install(easy_install):

	def initialize_options(self):
		easy_install.initialize_options(self)

		self.index_url = 'file://' + os.path.abspath(LIB_INFO_DIR)
		self.index_url = self.index_url.replace('\\', '/')
		self.build_directory = '..'


	def finalize_options(self):
		easy_install.finalize_options(self)

		if self.pth_file:
			instdir = normalize_path(self.install_dir)
			self.pth_file.filename = os.path.join(instdir, PTH_FILE_NAME)

		# fix PackageIndex._download_svn()
		# ...


	def easy_install(self, spec, deps=False):
		lib_name = get_lib_name(LIB_INFO_DIR, spec)
		try:
			return easy_install.easy_install(self, lib_name, deps)
		except BaseException as e:
			print('Exception: %r' % e)
		finally:
			self.clean_build_files(lib_name)


	def clean_build_files(self, lib_name):
		setup_base = os.path.join(self.build_directory, lib_name)
		paths = [
			os.path.join(setup_base, 'setup.py'),
			os.path.join(setup_base, 'setup.cfg'),
			os.path.join(setup_base, 'temp'),
			os.path.join(setup_base, 'build'),
			os.path.join(setup_base, lib_name + '.egg-info'),
		]
		clean_files(paths)


	def maybe_move(self, spec, dist_filename, src):
		dist = get_dist(spec, self.package_index, self.editable, not self.always_copy)
		basename = '%s-%s' % (dist.project_name, dist.version)
		setup_base = os.path.join(self.build_directory, dist.project_name)

		def maybe_move_instead(src):
			contents = os.listdir(src)
			if len(contents)==1:
				dist_filename = os.path.join(src,contents[0])
				if os.path.isdir(dist_filename):
					# if the only thing there is a directory, move it instead
					src = dist_filename
			return src

		dst = os.path.join(setup_base, basename)
		if os.path.exists(dst):
			src = maybe_move_instead(src)
		else:
			if os.path.isdir(dist_filename):
				src = dist_filename
			else:
				if os.path.dirname(dist_filename)==src:
					os.unlink(dist_filename)	# get it out of the tmp dir
				src = maybe_move_instead(src)
			ensure_directory(dst)

		move_files(src, dst, shutil.ignore_patterns('.*'))
		generate_setup(dist, LIB_INFO_DIR, setup_base, basename)

		return setup_base


def _main():
	try:
		main(
			cmdclass={
				'easy_install': lib_install,
			},
		)
	except AttributeError:
		log.warn('Library is not supported.')
	except Exception as e:
		log.warn(e)
		raise


if __name__ == '__main__':
	_main()
