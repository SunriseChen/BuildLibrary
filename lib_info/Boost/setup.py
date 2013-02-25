#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, shutil


def pre_process():
	print('Install Boost...')
	print('$basename')
	os.chdir('$basename')
	subprocess.call(['bootstrap.bat'])
	subprocess.call(['b2.exe'])
	shutil.rmtree('bin.v2')
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
