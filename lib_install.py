#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, tempfile
from setuptools import Command
from setuptools.package_index import PackageIndex, URL_SCHEME
from distutils import log
from distutils.errors import *
from pkg_resources import *


class lib_install(Command):
	description = 'find/get/install Library'
	command_consumes_arguments = True

	user_options = [
		('install-dir=', 'd', 'install lib to DIR'),
		('build-directory=', 'b',
			'download/extract/build in DIR; keep the results'),
	]
	create_index = PackageIndex

	def initialize_options(self):
		self.install_dir = self.build_directory = '../'
		self.args = None

		self.package_index = None

		self.verbose = self.distribution.verbose
		self.distribution._set_command_options(
			self, self.distribution.get_option_dict('lib_install')
		)

	def finalize_options(self):
		index_url = ''
		self.shadow_path = []
		for path_item in [self.install_dir, self.build_directory]:
			if path_item not in self.shadow_path:
				self.shadow_path.insert(0, path_item)
		if self.package_index is None:
			self.package_index = self.create_index(
				index_url, search_path=self.shadow_path
			)
		self.local_index = Environment(self.shadow_path + sys.path)

		if not self.args:
			raise DistutilsArgError(
				'No urls, filenames, or requirements specified (see --help)')

		self.outputs = []

	def run(self):
		if self.verbose != self.distribution.verbose:
			log.set_verbosity(self.verbose)
		try:
			for spec in self.args:
				self.lib_install(spec)
		finally:
			log.set_verbosity(self.distribution.verbose)

	def lib_install(self, spec, deps=False):
		tmpdir = tempfile.mkdtemp(prefix='lib_install-')
		download = None

		try:
			if not isinstance(spec, Requirement):
				if URL_SCHEME(spec):
					download = self.package_index.download(spec, tmpdir)
					return self.install_item(None, download, tmpdir, deps, True)
				elif os.path.exists(spec):
					return self.install_item(None, spec, tmpdir, deps, True)
				else:
					print(spec)
					from setuptools.command.easy_install import parse_requirement_arg
					spec = parse_requirement_arg(spec)

			print(spec)
			#dist = self.package_index.fetch_distribution(
			#	spec, tmpdir, self.upgrade, self.editable, not self.always_copy,
			#	self.local_index
			#)
			#if dist is None:
			#	msg = 'Could not find suitable distribution for %r' % spec
			#	if self.always_copy:
			#		msg+=' (--always-copy skips system and development eggs)'
			#	raise DistutilsError(msg)
			#elif dist.precedence==DEVELOP_DIST:
			#	# .egg-info dists don't need installing, just process deps
			#	self.process_distribution(spec, dist, deps, 'Using')
			#	return dist
			#else:
			#	return self.install_item(spec, dist.location, tmpdir, deps)

		finally:
			if os.path.exists(tmpdir):
				#rmtree(tmpdir)
				pass

	def install_item(self, spec, download, tmpdir, deps, install_needed=False):
		print(spec)

def main(argv=None, **kw):
    from setuptools import setup
    from setuptools.dist import Distribution
    import distutils.core

    USAGE = '''\
usage: %(script)s [options] requirement_or_url ...
   or: %(script)s --help
'''

    def gen_usage(script_name):
        script = os.path.basename(script_name)
        return USAGE % vars()

    def with_ei_usage(f):
        old_gen_usage = distutils.core.gen_usage
        try:
            distutils.core.gen_usage = gen_usage
            return f()
        finally:
            distutils.core.gen_usage = old_gen_usage

    class DistributionWithoutHelpCommands(Distribution):
        common_usage = ""
        def _show_help(self, *args, **kw):
            with_ei_usage(lambda: Distribution._show_help(self, *args, **kw))

    if argv is None:
        argv = sys.argv[1:]

    with_ei_usage(lambda:
        setup(
            script_name = sys.argv[0] or 'lib_install',
            script_args = ['-q', 'lib_install', '-v'] + argv,
			#entry_points = {
			#	'distutils.commands': [
			#		'lib_install = lib_install:lib_install',
			#	],
			#},
			cmdclass = {
				'lib_install': lib_install,
			},
            distclass = DistributionWithoutHelpCommands, **kw
        )
    )


if __name__ == '__main__':
	main()
