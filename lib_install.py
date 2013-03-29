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

	print('Downloading ' + url)
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
	subprocess.call(['python', setuptools])
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
	if sys.platform.startswith('win'):
		subprocess.call(['easy_install', 'SCons'])
	elif os.uname()[1] == 'Debian':
		subprocess.call(['apt-get', '-y', 'install', 'scons'])
	else:
		subprocess.call(['yum', '-y', 'install', 'scons'])
	#restart()


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


def move_update_files(src_dir, dst_dir, ignore=None):
	names = os.listdir(src_dir)
	if ignore is not None:
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
			move_update_files(src_name, dst_name, ignore)
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
	move_update_files(unpack_dir, os.curdir,
		shutil.ignore_patterns('.git*', '*.sln', '*.pyproj', '*.sample'))
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
	print('compiler = %s' % ccompiler.get_default_compiler(os.name, sys.platform))

	from SCons.Environment import Environment
	env = Environment()
	vars = [
		'CC',
		'CXX',
		'PLATFORM',
		'MSVC_VERSION',
		'TARGET_ARCH',
		'MSVS',
		'MSVS_VERSION',
		'MSVS_ARCH',
		'TOOLS',
	]
	for var in vars:
		print('%s = %r' % (var, env.subst('$' + var)))


def print_object(obj):
	for item in obj.__dict__.items():
		print('%s = %r' % item)


def get_dist_directory(dist):
	from setuptools.package_index import egg_info_for_url, EXTENSIONS

	basename, fragment = egg_info_for_url(dist.location)
	for ext in EXTENSIONS:
		if basename.endswith(ext):
			basename = basename[:-len(ext)]
			return os.path.basename(basename)


def test():
	from setuptools.package_index import distros_for_url

	dists = distros_for_url('http://sourceforge.net/projects/boost/files/boost/1.53.0/boost_1_53_0.tar.bz2%23egg=Boost-1.53.0#md5=a00d22605d5dbcfb4c9936a9b35bc4c2')
	#dists = distros_for_url('http://sourceforge.net/projects/boost/files/boost/1.53.0/boost_1_53_0.tar.bz2#egg=Boost-1.53.0')
	#dists = distros_for_url('file:C:\\sourceforge.net\\projects\\boost\\files\\boost\\1.53.0\\boost_1_53_0.tar.bz2#egg=Boost-1.53.0')
	for dist in dists:
		print('========\n%r' % dist)
		print_object(dist)
		#print(get_dist_directory(dist))
		print_object(dist._provider)


check_env()
#show_sys_vars()
#test()
#exit()


from setuptools.command.easy_install import *
from setuptools.command.easy_install import rmtree
from pkg_resources import *
from distutils import log
#from distutils.errors import *

class lib_install(easy_install):

	def initialize_options(self):
		easy_install.initialize_options(self)

		self.index_url = 'file:' + LIB_INFO_DIR
		self.build_directory = '..'

	def finalize_options(self):
		easy_install.finalize_options(self)

		if self.pth_file:
			instdir = normalize_path(self.install_dir)
			self.pth_file.filename = os.path.join(instdir, PTH_FILE_NAME)

	def easy_install(self, spec, deps=False):
		return self.lib_install(spec, deps)

	def lib_install(self, spec, deps):
		from setuptools.command.easy_install import parse_requirement_arg
		from setuptools.package_index import URL_SCHEME

		tmpdir = tempfile.mkdtemp(prefix=TEMP_DIR_PREFIX)
		download = None
		if not self.editable: self.install_site_py()

		try:
			dist = None
			if not isinstance(spec, Requirement):
				if URL_SCHEME(spec):
					# It's a url, download it to tmpdir and process
					self.not_editable(spec)
					download = self.package_index.download(spec, tmpdir)
					return self.install_item(None, download, tmpdir, deps, True)

				elif os.path.exists(spec):
					# Existing file or directory, just process it directly
					self.not_editable(spec)
					return self.install_item(None, spec, tmpdir, deps, True)
				else:
					spec = parse_requirement_arg(spec)

			self.check_editable(spec)
			dist = self.package_index.fetch_distribution(
				spec, tmpdir, self.upgrade, self.editable, not self.always_copy,
				self.local_index
			)
			if dist is None:
				msg = "Could not find suitable distribution for %r" % spec
				if self.always_copy:
					msg+=" (--always-copy skips system and development eggs)"
				raise DistutilsError(msg)
			elif dist.precedence==DEVELOP_DIST:
				# .egg-info dists don't need installing, just process deps
				self.process_distribution(spec, dist, deps, "Using")
				return dist
			else:
				self.generate_setup(dist, tmpdir)
				return self.install_item(spec, dist.location, tmpdir, deps)

		finally:
			if os.path.exists(tmpdir):
				rmtree(tmpdir)
			if dist:
				self.clean_build_files(dist.project_name)

	def generate_setup(self, dist, setup_base):
		from string import Template

		src_file = os.path.join(LIB_INFO_DIR, dist.project_name, 'setup.py')
		setup_script = os.path.join(setup_base, 'setup.py')
		with open(setup_script, 'w') as dst:
			with open(src_file) as src:
				basename = self.get_dist_basename(dist)
				for line in src:
					line = Template(line).safe_substitute(
						version=dist.version,
						basename=basename,
					)
					dst.write(line)
		return setup_script

	def clean_build_files(self, project_name):
		setup_base = os.path.join(self.build_directory, project_name)
		paths = [
			os.path.join(setup_base, 'temp'),
			os.path.join(setup_base, 'build'),
			os.path.join(setup_base, project_name + '.egg-info'),
			os.path.join(setup_base, 'setup.py'),
			os.path.join(setup_base, 'setup.cfg'),
		]
		for path in paths:
			if os.path.exists(path):
				if os.path.isfile(path):
					os.remove(path)
				elif os.path.isdir(path):
					rmtree(path)

	def get_dist_basename(self, dist):
		from setuptools.package_index import egg_info_for_url, EXTENSIONS

		basename, fragment = egg_info_for_url(dist.location)
		for ext in EXTENSIONS:
			if basename.endswith(ext):
				basename = basename[:-len(ext)]
				return os.path.basename(basename)


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
