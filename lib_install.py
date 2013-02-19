#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ez_setup import use_setuptools
use_setuptools()

import os, sys, tempfile
from setuptools.command.easy_install import *
from setuptools.command.easy_install import rmtree, parse_requirement_arg
from setuptools.package_index import URL_SCHEME
from distutils import log
from distutils.errors import *
from pkg_resources import *

LIB_INFO_DIR = 'lib_info'


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
		self.lib_install(spec, deps)

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
