#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from setuptools import Command
from setuptools.package_index import PackageIndex, URL_SCHEME
from distutils.errors import *


class lib_install(Command):

	user_options = [
		('install-dir=', 'd', 'install lib to DIR'),
		('build-directory=', 'b',
			'download/extract/build in DIR; keep the results'),
	]
	create_index = PackageIndex

	def initialize_options(self):
		self.install_dir = None
		self.build_directory = None

		self.package_index = None

		self.verbose = self.distribution.verbose
		self.distribution._set_command_options(
			self, self.distribution.get_option_dict('lib_install')
		)

	def finalize_options(self):
		index_url = ''
		if self.package_index is None:
			self.package_index = self.create_index(
				index_url, search_path=self.shadow_path
			)
		self.local_index = Environment(self.shadow_path + sys.path)

	def run(self):
		print('lib_install')


def main(argv=None, **kw):
    from setuptools import setup
    from setuptools.dist import Distribution
    import distutils.core

    USAGE = """\
usage: %(script)s [options] requirement_or_url ...
   or: %(script)s --help
"""

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
            script_args = ['-q','lib_install', '-v']+argv,
            script_name = sys.argv[0] or 'lib_install',
            distclass=DistributionWithoutHelpCommands, **kw
        )
    )


if __name__ == '__main__':
	main()
