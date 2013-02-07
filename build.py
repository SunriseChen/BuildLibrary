#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, shutil
from setuptools import setup
from pkg_resources import parse_version

LIB_INFO_DIR = 'lib_info'


def get_lib_info():
	lib_info = {}
	for root, dirs, files in os.walk(LIB_INFO_DIR):
		for f in files:
			mod_name, ext = os.path.splitext(f)
			if ext.lower() == '.py' and not mod_name.lower().endswith('__init__'):
				mod_name = os.path.join(root, mod_name)
				mod_name = mod_name.replace('\\', '.')
				mod_name = mod_name.replace('/', '.')
				# from mod_name import add_lib_info
				mod = __import__(mod_name, globals(), locals(), ['add_lib_info'])
				if hasattr(mod, 'add_lib_info'):
					mod.add_lib_info(lib_info)
	
	return lib_info


def add_lib_info(lib_info, **attrs):
	name = attrs.get('name')
	version = attrs.get('version')
	if name is None or version is None:
		raise DistutilsSetupError('name and version must be provided.')

	name = name.lower()
	version = parse_version(version)
	if name in lib_info:
		lib_info[name][version] = attrs
	else:
		lib_info[name] = { version: attrs }

	return attrs


def get_local_version(dist_list):
	return parse_version('5.2.0')


def get_dist_info(lib_info, name, version=None, cmp=None):
	if name not in lib_info:
		return None

	version_list = sorted(lib_info[name].iterkeys(), reverse=True)
	if version is None:
		version = version_list[0]
	if cmp is None:
		cmp = '>='

	local_version = get_local_version(lib_info)
	if cmp == '==' and local_version == version or	\
		cmp == '!=' and local_version != version or	\
		cmp == '>' and local_version > version or	\
		cmp == '>=' and local_version >= version or	\
		cmp == '<' and local_version < version or	\
		cmp == '<=' and local_version <= version:
		print('Current version is your need.')
		return None

	for remote_version in version_list:
		if cmp == '==' and remote_version == version or		\
			cmp == '!=' and remote_version != version or	\
			cmp == '>' and remote_version > version or		\
			cmp == '>=' and remote_version >= version or	\
			cmp == '<' and remote_version < version or		\
			cmp == '<=' and remote_version <= version:
			return lib_info[name][remote_version]

	print('Did not comply with the version.')
	return None


#def install(dist_list, version=None, cmp=None):
#	lib_dist = get_lib_dist(dist_list, version, cmp)
#	if lib_dist:
#		from bl_setup import download_and_validate, unpack_file
#		download_url = lib_dist.get_download_url()
#		file_digest = lib_dist.get_file_digest()
#		target_dir = '../' + lib_dist.get_name()
#		file_name = download_and_validate(download_url, file_digest, target_dir)
#		if file_name:
#			unpack_dir = unpack_file(file_name, target_dir)
#			print(lib_dist.packages)
#			print(lib_dist.cmdclass)
#			move_files(PACK_FILE_ROOT_DIR, os.curdir, shutil.ignore_patterns('.git*'))
#			shutil.rmtree(PACK_FILE_ROOT_DIR)
#			os.remove(file_name)
#
#		#pack_file = lib_dist.download(download_url)
#		#unpack_dir = lib_dist.unpack(pack_file)
#		lib_dist.build(unpack_dir)
#		lib_dist.install(unpack_dir)
#		lib_dist.clean()


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
		name = lib_params[0].lower()
		version = lib_params[3]
		cmp = lib_params[2]
		if version:
			version = parse_version(version)
		if name in lib_info:
			dist_info = get_dist_info(lib_info, name, version, cmp)
			if dist_info:
				setup(
					script_name=sys.argv[0] or __file__,
					script_args=['install'],
					**dist_info)
		else:
			print(lib + ' is not supported.')


if __name__ == '__main__':
	main()
