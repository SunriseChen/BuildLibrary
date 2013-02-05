#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from pkg_resources import parse_version

LIB_INFO_DIR = 'lib_info'


def get_lib_info():
	lib_info = {}
	for root, dirs, files in os.walk(LIB_INFO_DIR):
		for f in files:
			lib_name, ext = os.path.splitext(f)
			if ext.lower() == '.py' and not lib_name.lower().endswith('__init__'):
				lib_name = os.path.join(root, lib_name)
				lib_name = lib_name.replace('\\', '.')
				lib_name = lib_name.replace('/', '.')
				# from lib_name import get_dist_list
				lib = __import__(lib_name, globals(), locals(), ['get_dist_list'])
				if hasattr(lib, 'get_dist_list'):
					lib_info[lib_name[9:].lower()] = lib.get_dist_list()
	
	return lib_info


def get_local_version(dist_list):
	return parse_version('5.2.1')


def get_lib_dist(dist_list, version=None, cmp=None):
	#sorted(dist_list)

	if version is None:
		version = dist_list[0].get_version()
	if cmp is None:
		cmp = '>='

	version = parse_version(version)
	local_version = get_local_version(dist_list)
	if cmp == '==' and local_version == version or	\
		cmp == '!=' and local_version != version or	\
		cmp == '>' and local_version > version or	\
		cmp == '>=' and local_version >= version or	\
		cmp == '<' and local_version < version or	\
		cmp == '<=' and local_version <= version:
		print('Current version is your need.')
		return None

	for dist in dist_list:
		remote_version = parse_version(dist.get_version())
		if cmp == '==' and remote_version == version or		\
			cmp == '!=' and remote_version != version or	\
			cmp == '>' and remote_version > version or		\
			cmp == '>=' and remote_version >= version or	\
			cmp == '<' and remote_version < version or		\
			cmp == '<=' and remote_version <= version:
			return dist

	print('Did not comply with the version.')
	return None


def install(dist_list, version=None, cmp=None):
	lib_dist = get_lib_dist(dist_list, version, cmp)
	if lib_dist:
		pack_file = lib_dist.download(download_url)
		unpack_dir = lib_dist.unpack(pack_file)
		lib_dist.build(unpack_dir)
		lib_dist.install(unpack_dir)
		lib_dist.clean()


def main():
	import argparse, subprocess, re

	lib_info = get_lib_info()

	parser = argparse.ArgumentParser(description='build lib')
	parser.add_argument('lib', metavar='lib', nargs='+',
			help='Library name')

	args = parser.parse_args()
	libPattern = re.compile(r'^(.+?)((==|!=|>|>=|<|<=)(.*))?$')
	for lib in args.lib:
		lib_params = libPattern.search(lib).groups()
		lib_name = lib_params[0].lower()
		lib_version = lib_params[3]
		cmp = lib_params[2]
		if lib_name in lib_info:
			install(lib_info[lib_name], lib_version, cmp)
		else:
			print(lib + ' is not supported.')


if __name__ == '__main__':
	main()
