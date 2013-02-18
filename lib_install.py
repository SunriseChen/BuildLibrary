#! /usr/bin/env python
# -*- coding: utf-8 -*-

#import os, sys, tempfile
#from setuptools import Command
from setuptools.command.easy_install import easy_install, main
#from setuptools.package_index import PackageIndex, URL_SCHEME
from distutils import log
#from distutils.errors import *
#from pkg_resources import *


class lib_install(easy_install):

	def initialize_options(self):
		easy_install.initialize_options(self)
		self.index_url = 'file:lib_info'
		#self.find_links = 'file:lib_info/index.html'

	def finalize_options(self):
		easy_install.finalize_options(self)
		print('finalize_options')

	def run(self):
		print('run')
		easy_install.run(self)

	def lib_install(self, spec, deps=False):
		pass

	def install_item(self, spec, download, tmpdir, deps, install_needed=False):
		print(spec)
		easy_install.install_item(self, spec, download, tmpdir, deps, install_needed)


def _main():
	try:
		main(
			cmdclass = {
				'easy_install': lib_install,
			},
		)
	except AttributeError:
		log.warn('Library is not supported.')
	except Exception as e:
		log.warn(e)


if __name__ == '__main__':
	_main()
