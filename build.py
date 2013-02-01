#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, shutil
from distutils.dist import Distribution
from distutils.core import run_setup


def make_lib_info():
	libs = []
	for root, dirs, files in os.walk('library_info'):
		for f in files:
			lib_name, ext = os.path.splitext(f)
			if ext.lower() == '.py' and not lib_name.lower().endswith('__init__'):
				lib_info_path = os.path.join(root, f)
				libs.append(lib_info_path)
	
	return libs


class LibraryDistribution(Distribution):
	pass
	#lib_dist = run_setup(lib_info_path, stop_after='commandline')

	#find()
	#compare()
	#download()
	#unpack()
	#build()
	#install()
	#clean()


def main():
	import argparse

	parser = argparse.ArgumentParser(description='build lib')
	parser.add_argument('lib_name', metavar='lib', nargs='+',
			help='Library name')

	args = parser.parse_args()
	print(args.lib_name)


if __name__ == '__main__':
	main()
	print make_lib_info()
