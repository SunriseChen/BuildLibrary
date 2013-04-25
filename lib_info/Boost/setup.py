#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess
from common import *


def build(version):
	bootstrap_command = ['./bootstrap.sh', '--prefix=/usr/local/']
	build_command = ['./b2', 'install']

	env = Environment()
	if env.platform == 'win32':
		bootstrap_command = ['bootstrap.bat']
		build_command = ['b2.exe']

	#subprocess.call(bootstrap_command)
	#subprocess.call(build_command)

	clean_list = [
		'bin.v2',
		'tools/build/v2/engine/bin.*',
		'tools/build/v2/engine/bootstrap',
	]
	clean_files(clean_list)

	os.environ['INCLUDE_PATH'] = os.pathsep.join([
		'.',
	])
	os.environ['LIBRARY_PATH'] = os.pathsep.join([
		'stage/lib',
	])

	return True


def main():
	from distutils.version import LooseVersion

	name = '$name'
	version = LooseVersion('$version')
	os.chdir('$lib_name')

	print('Building %s %s ...' % (name, version))
	if build(version):
		os.chdir('..')

		from setuptools import setup
		setup(
			name=name,
			version=str(version),

			author='Boost',
			author_email=' ',
			description='Boost provides free portable peer-reviewed C++ libraries. The emphasis is on portable libraries which work well with the C++ Standard Library. See http://www.boost.org',
			license='Boost Software License',
			url='http://www.boost.org',
		)
	else:
		sys.exit(1)


if __name__ == '__main__':
	main()
