#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, shutil


def pre_process():
	from common import Environment

	print('Install Boost...')
	os.chdir('$basename')

	env = Environment()
	bootstrap_command = ['bootstrap.bat']
	build_command = ['b2.exe']

	if env.platform[:3] != 'win':
		bootstrap_command = ['bootstrap.sh', '--prefix=/usr/local/']
		build_command = ['b2', 'install']

	subprocess.call(bootstrap_command)
	subprocess.call(build_command)
	shutil.rmtree('bin.v2')
	#shutil.rmtree('tools/build/v2/engine/bin.*')
	shutil.rmtree('tools/build/v2/engine/bootstrap')
	os.chdir('..')


def post_process():
	print('post process.')


def main():
	pre_process()

	from setuptools import setup
	setup(
		name='Boost',
		version='$version',

		author='Boost',
		author_email=' ',
		description='Boost provides free portable peer-reviewed C++ libraries. The emphasis is on portable libraries which work well with the C++ Standard Library. See http://www.boost.org',
		license='Boost Software License',
		url='http://www.boost.org',
	)

	post_process()


if __name__ == '__main__':
	main()
