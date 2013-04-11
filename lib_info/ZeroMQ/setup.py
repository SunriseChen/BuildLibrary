#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess
from common import *


def build(version):
	print('Install ZeroMQ...')

	env = Environment()
	if env.compiler == 'msvc':
		sln_file = r'builds\msvc\msvc%s.sln'
		build_params = []
		if env.compiler_version > '10.0':
			shutil.copy2(sln_file % '10', sln_file % '11')
			sln_file = sln_file % '11'
			build_params += [['/upgrade']]
		elif env.compiler_version > '9.0':
			sln_file = sln_file % '10'
		else:
			sln_file = sln_file % ''

		build_params += [
			['/rebuild', '"debug|win32"'],
			['/rebuild', '"release|win32"'],
			['/rebuild', '"debug|x64"'],
			['/rebuild', '"release|x64"'],
		]
		for params in build_params:
			cmd = ['devenv', sln_file] + params
			print(cmd)
			subprocess.call(cmd, shell=True)
	else:
		env.configure()
		#env.make('clean', 'install')
		env.make('install')

	clean_files('obj')

	return True


def main():
	from distutils.version import LooseVersion

	version = LooseVersion('$version')
	os.chdir('$basename')
	if build(version):
		os.chdir('..')
		print(os.path.abspath(os.curdir))

		from setuptools import setup
		setup(
			name='ZeroMQ',
			version='$version',

			author='iMatix Corporation',
			author_email='zeromq-dev@lists.zeromq.org',
			description='''The socket library that acts as a concurrency framework. Faster than TCP, for clustered products and supercomputing. Carries messages across inproc, IPC, TCP, and multicast. Connect N-to-N via fanout, pubsub, pipeline, request-reply. Asynch I/O for scalable multicore message-passing apps. Large and active open source community. 30+ languages including C, C++, Java, .NET, Python. Most OSes including Linux, Windows, OS X. LGPL free software with full commercial support from iMatix.''',
			license='LGPL',
			url='http://zeromq.org',
		)


if __name__ == '__main__':
	main()
