#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os


def pre_process():
	from common import Environment, clean_files

	print('Install ZeroMQ...')
	os.chdir('$basename')

	env = Environment()

	config_parameter = []
	if env.platform.startswith('win'):
		if env.compiler == 'msvc':
			if float(env.compiler_version) > 9:
				config_parameter.append('msvc9')
			elif env.compiler_version[:3] == '7.1':
				config_parameter.append('msvc71')
			else:
				config_parameter.append('msvc' + env.compiler_version[0])

	config_parameter += ['--with-static-rtl', '--with-dynamic-rtl']
	#env.configure(config_parameter)
	#os.chdir('build/lib')
	#env.make('clean', 'install')

	#clean_files('obj')
	os.chdir('..')


def post_process():
	print('post process.')


def main():
	pre_process()

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

	post_process()


if __name__ == '__main__':
	main()
