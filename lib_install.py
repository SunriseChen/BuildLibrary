#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, tempfile

EZ_SETUP_URL = 'http://peak.telecommunity.com/dist/ez_setup.py'
LIB_INFO_DIR = 'lib_info'


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


def install_setuptools():
	print('install setuptools...')
	ez_setup = download_file(EZ_SETUP_URL)
	import subprocess
	subprocess.call(['python', ez_setup])
	import site
	for path in site.getsitepackages():
		site.addsitedir(path)


try:
	import setuptools
except ImportError:
	install_setuptools()


from setuptools.command.easy_install import *
from setuptools.command.easy_install import rmtree, parse_requirement_arg
from setuptools.package_index import URL_SCHEME
from distutils import log
from distutils.errors import *
from pkg_resources import *


class lib_install(easy_install):

	def initialize_options(self):
		easy_install.initialize_options(self)
		self.index_url = 'file:' + LIB_INFO_DIR
		self.build_directory = '..'

	def finalize_options(self):
		try:
			easy_install.finalize_options(self)
		except DistutilsArgError:
			if not self.args:
				print('self update')

		if self.pth_file:
			instdir = normalize_path(self.install_dir)
			self.pth_file.filename = os.path.join(instdir, 'lib-install.pth')

	def easy_install(self, spec, deps=False):
		return self.lib_install(spec, deps)

	def lib_install(self, spec, deps):
		tmpdir = tempfile.mkdtemp(prefix="lib_install-")
		download = None
		if not self.editable: self.install_site_py()

		try:
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

	def install_item(self, spec, download, tmpdir, deps, install_needed=False):

		# Installation is also needed if file in tmpdir or is not an egg
		install_needed = install_needed or self.always_copy
		install_needed = install_needed or os.path.dirname(download) == tmpdir
		install_needed = install_needed or not download.endswith('.egg')
		install_needed = install_needed or (
			self.always_copy_from is not None and
			os.path.dirname(normalize_path(download)) ==
			normalize_path(self.always_copy_from)
		)

		if spec and not install_needed:
			# at this point, we know it's a local .egg, we just don't know if
			# it's already installed.
			for dist in self.local_index[spec.project_name]:
				if dist.location==download:
					break
			else:
				install_needed = True   # it's not in the local index

		log.info("Processing %s", os.path.basename(download))

		if install_needed:
			dists = self.install_eggs(spec, download, tmpdir)
			for dist in dists:
				self.process_distribution(spec, dist, deps)
		else:
			dists = [self.check_conflicts(self.egg_distribution(download))]
			self.process_distribution(spec, dists[0], deps, "Using")

		if spec is not None:
			for dist in dists:
				if dist in spec:
					return dist

	def run_setup(self, setup_script, setup_base, args):
		from setuptools.command import bdist_egg, egg_info
		from setuptools.sandbox import run_setup

		sys.modules.setdefault('distutils.command.bdist_egg', bdist_egg)
		sys.modules.setdefault('distutils.command.egg_info', egg_info)

		args = list(args)
		if self.verbose>2:
			v = 'v' * (self.verbose - 1)
			args.insert(0,'-'+v)
		elif self.verbose<2:
			args.insert(0,'-q')
		if self.dry_run:
			args.insert(0,'-n')
		log.info(
			"Running %s %s", setup_script[len(setup_base)+1:], ' '.join(args)
		)
		try:
			run_setup(setup_script, args)
		except SystemExit, v:
			raise DistutilsError("Setup script exited with %s" % (v.args[0],))

	def generate_setup(self, dist, setup_base):
		from string import Template

		src_file = os.path.join(LIB_INFO_DIR, dist.project_name, 'setup.py')
		setup_script = os.path.join(setup_base, 'setup.py')
		with open(setup_script, 'w') as dst:
			with open(src_file) as src:
				for line in src:
					line = Template(line).safe_substitute(
						version=dist.version,
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
		]
		for path in paths:
			if os.path.exists(path):
				if os.path.isfile(path):
					os.remove(path)
				elif os.path.isdir(path):
					rmtree(path)


def _main():
	#try:
		main(
			cmdclass={
				'easy_install': lib_install,
			},
		)
	#except AttributeError:
	#	log.warn('Library is not supported.')
	#except Exception as e:
	#	log.warn(e)


if __name__ == '__main__':
	_main()
