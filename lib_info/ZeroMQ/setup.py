#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess
from common import *


def build(version):
	env = Environment()
	if env.compiler == 'msvc':
		sln_file = r'builds\msvc\msvc%s.sln'
		if env.compiler_version > '10.0':
			shutil.copy2(sln_file % '10', sln_file % '11')
			sln_file %= '11'
			subprocess.call(['devenv', sln_file, '/upgrade'])
			clean_list = [
				r'builds\msvc\Backup',
				r'builds\msvc\_Upgrade*',
				r'builds\msvc\Upgrade*',
			]
			clean_files(clean_list)
		elif env.compiler_version > '9.0':
			sln_file %= '10'
		else:
			sln_file %= ''

		build_params = [
			'/p:Configuration=Debug;Platform=Win32',
			'/p:Configuration=Release;Platform=Win32',
			'/p:Configuration=Debug;Platform=x64',
			'/p:Configuration=Release;Platform=x64',
		]
		for param in build_params:
			subprocess.call(['msbuild', sln_file, '/m', '/t:rebuild', param])
	else:
		env.configure()
		env.make('install')

	clean_files('obj')

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

			author='iMatix Corporation',
			author_email='zeromq-dev@lists.zeromq.org',
			description='''The socket library that acts as a concurrency framework. Faster than TCP, for clustered products and supercomputing. Carries messages across inproc, IPC, TCP, and multicast. Connect N-to-N via fanout, pubsub, pipeline, request-reply. Asynch I/O for scalable multicore message-passing apps. Large and active open source community. 30+ languages including C, C++, Java, .NET, Python. Most OSes including Linux, Windows, OS X. LGPL free software with full commercial support from iMatix.''',
			license='LGPL',
			url='http://zeromq.org',
		)
	else:
		sys.exit(1)


if __name__ == '__main__':
	main()
