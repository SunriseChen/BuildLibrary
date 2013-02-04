#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os


def get_lib_info():
	lib_info = {}
	for root, dirs, files in os.walk('lib_info'):
		for f in files:
			lib_name, ext = os.path.splitext(f)
			if ext.lower() == '.py' and not lib_name.lower().endswith('__init__'):
				lib_name = os.path.join(root[9:], lib_name).lower()
				lib_name = lib_name.replace('\\', '.')
				lib_name = lib_name.replace('/', '.')
				lib_info_path = os.path.join(root, f)
				lib_info[lib_name] = lib_info_path
	
	return lib_info


def install(lib_name, lib_version=None):
	lib_dist = __import__(lib_name)
	download_url = lib_dist.find(lib_version)
	if download_url:
		pack_file = lib_dist.download(download_url)
		unpack_dir = lib_dist.unpack(pack_file)
		lib_dist.build(unpack_dir)
		lib_dist.install(unpack_dir)
		lib_dist.clean()
	else:
		print('Current version is your need.')


def main():
	import argparse
	import subprocess

	lib_info = get_lib_info()

	parser = argparse.ArgumentParser(description='build lib')
	parser.add_argument('lib', metavar='lib', nargs='+',
			help='Library name')

	args = parser.parse_args()
	for lib in args.lib:
		lib_name = lib.lower()
		if lib_name in lib_info:
			subprocess.call(['python', lib_info[lib_name], 'install'])
		else:
			print(lib + ' is not supported.')


if __name__ == '__main__':
	main()
