#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, tempfile, shutil

DEFAULT_VERSION = '0.1.0'
DEFAULT_URL     = 'https://github.com/SunriseChen/BuildLibrary/archive/master.zip'
PACK_FILE_ROOT_DIR = 'BuildLibrary-master'

SETUPTOOLS_URL = 'http://python-distribute.org/distribute_setup.py'
PYTHON_ENV = 'pyenv'
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


def install_virtualenv():
	print('Install virtualenv...')
	if subprocess.call(['easy_install', 'virtualenv']) == 0:
		restart()


def virtual_run(commands):
	suffix = '.bat' if sys.platform == 'win32' else '.sh'
	fd, path = tempfile.mkstemp(suffix=suffix, dir=os.curdir)
	try:
		f = os.fdopen(fd, 'w')
		if not isinstance(commands, list):
			commands = [commands]

		if sys.platform == 'win32':
			commands.insert(0, '@echo off')
			commands.insert(1, 'call %s/Scripts/activate.bat' % PYTHON_ENV)
			commands.append('call %s/Scripts/deactivate.bat' % PYTHON_ENV)
		else:
			commands.insert(0, 'source %s/bin/activate' % PYTHON_ENV)
			commands.append('%s/bin/deactivate' % PYTHON_ENV)

		commands = os.linesep.join(commands)
		f.write(commands)
		f.close()

		return subprocess.call([path])
	finally:
		if os.path.exists(path):
			os.remove(path)


def validate_pair(ob):
	try:
		if not (len(ob) == 2):
			print("Unexpected result:", ob)#, file=sys.stderr)
			raise ValueError
	except:
		return False
	return True

def consume(iter):
	try:
		while True: next(iter)
	except StopIteration:
		pass

def get_environment_from_batch_command(env_cmd, initial=None):
	"""
	Take a command (either a single command or list of arguments)
	and return the environment created after running that command.
	Note that if the command must be a batch file or .cmd file, or the
	changes to the environment will not be captured.

	If initial is supplied, it is used as the initial environment passed
	to the child process.
	"""
	if not isinstance(env_cmd, (list, tuple)):
		env_cmd = [env_cmd]
	# construct the command that will alter the environment
	env_cmd = subprocess.list2cmdline(env_cmd)
	# create a tag so we can tell in the output when the proc is done
	tag = 'Done running command'
	# construct a cmd.exe command to do accomplish this
	cmd = 'cmd.exe /s /c "{env_cmd} && echo "{tag}" && set"'.format(**vars())
	# launch the process
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=initial)
	# parse the output sent to stdout
	lines = proc.stdout
	# consume whatever output occurs until the tag is reached
	consume(itertools.takewhile(lambda l: tag not in l, lines))
	# define a way to handle each KEY=VALUE line
	handle_line = lambda l: l.rstrip().split('=',1)
	# parse key/values into pairs
	pairs = map(handle_line, lines)
	# make sure the pairs are valid
	valid_pairs = filter(validate_pair, pairs)
	# construct a dictionary of the pairs
	result = dict(valid_pairs)
	# let the process finish
	proc.communicate()
	return result


def check_virtualenv(times=3):
	for i in range(times):
		try:
			import virtualenv
			if not os.path.exists(PYTHON_ENV):
				subprocess.call(['virtualenv', '--distribute', PYTHON_ENV])
			break
		except ImportError:
			install_virtualenv()
	else:
		print('Install virtualenv fail!')
		sys.exit(1)


def install_scons():
	print('Install SCons...')
	virtual_run('pip install SCons')


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

		if os.path.exists(dst_name):
			if os.path.isfile(dst_name):
				os.remove(dst_name)
			elif os.path.islink(dst_name):
				os.rmdir(dst_name)
			else:
				shutil.rmtree(dst_name)

		if os.path.islink(src_name):
			target = os.readlink(src_name)
			os.symlink(target, dst_name)
		elif os.path.isdir(src_name):
			move_files(src_name, dst_name, ignore)
		else:
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
	check_virtualenv()
	check_scons()
	sys.exit()
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
		project_name = get_project_name(LIB_INFO_DIR, spec)
		try:
			dist = easy_install.easy_install(self, project_name, deps)
			generate_import(self.build_directory, project_name, dist.version)
			return dist
		except BaseException as e:
			print('Exception: %r' % e)
		finally:
			self.clean_build_files(project_name)


	def clean_build_files(self, project_name):
		setup_base = os.path.join(self.build_directory, project_name)
		paths = [
			os.path.join(setup_base, 'setup.py'),
			os.path.join(setup_base, 'setup.cfg'),
			os.path.join(setup_base, 'temp'),
			os.path.join(setup_base, 'build'),
			os.path.join(setup_base, project_name + '.egg-info'),
		]
		clean_files(paths)


	def maybe_move(self, spec, dist_filename, src):
		if os.path.isdir(dist_filename):
			src = dist_filename
		else:
			if os.path.dirname(dist_filename)==src:
				os.unlink(dist_filename)	# get it out of the tmp dir
			contents = os.listdir(src)
			if len(contents)==1:
				dist_filename = os.path.join(src,contents[0])
				if os.path.isdir(dist_filename):
					# if the only thing there is a directory, move it instead
					src = dist_filename

		dist = get_dist(spec, self.package_index, self.editable,
			not self.always_copy)
		lib_name = get_lib_name(spec.project_name, dist.version)
		setup_base = os.path.join(self.build_directory, spec.project_name)
		dst = os.path.join(setup_base, lib_name)

		ensure_directory(dst)
		move_files(src, dst, shutil.ignore_patterns('.*'))
		generate_setup(LIB_INFO_DIR, spec.project_name, dist.version,
			setup_base)

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
