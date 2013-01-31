#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, shutil
#import subprocess

DEFAULT_VERSION = '0.1.0'
DEFAULT_URL     = 'https://github.com/SunriseChen/BuildLibrary/archive/master.zip'
MD5_DIGEST = 'b59cb88bd745078bcee4568b9162aaca'
PACK_FILE_ROOT_DIR = 'BuildLibrary-master'


def download_file(url, target_dir=os.curdir):
	from urllib2 import urlopen, URLError, HTTPError

	print('Downloading url: ' + url)
	remote_file = urlopen(url)

	file_name = os.path.basename(url)
	file_path = os.path.join(target_dir, file_name)
	with open(file_path, 'wb') as local_file:
		local_file.write(remote_file.read())

	remote_file.close()
	print('Downloaded.')

	return os.path.realpath(file_path)


def validate_md5(data, digest):
	try:
		# Python version >= 2.5
		from hashlib import md5
	except ImportError:
		# Python version < 2.5
		from md5 import md5

	#print(md5(data).hexdigest())
	return (digest == md5(data).hexdigest())


def validate_file(file_name, file_digest):
	with open(file_name, 'rb') as file_data:
		return validate_md5(file_data.read(), file_digest)

	return False


def download_and_validate(url, file_digest, target_dir=os.curdir, retry_times=3):
	for i in range(retry_times):
		file_name = download_file(url, target_dir)
		if validate_file(file_name, file_digest):
			return file_name

		print('Downloaded file validate failed.')

	print('Download and validate failed times overfull.')

	return None


def unpack_file(file_name, target_dir=os.curdir):
	import tarfile
	import zipfile

	print('Unpacking file: ' + file_name)
	if tarfile.is_tarfile(file_name):
		with tarfile.open(file_name) as tar_file:
			tar_file.extractall(target_dir)
	elif zipfile.is_zipfile(file_name):
		with zipfile.ZipFile(file_name) as zip_file:
			zip_file.extractall(target_dir)
	else:
		print('Pack file format is unknow. unpack fail!')
		sys.exit(1)

	print('Unpacked.')

	return os.path.realpath(target_dir)


def move_files(src_dir, dst_dir, ignore=None):
	names = os.listdir(src_dir)
	if ignore is not None:
		ignored_names = ignore(src_dir, names)
	else:
		ignored_names = set()

	for name in names:
		if name in ignored_names:
			continue
		src_name = os.path.join(src_dir, name)
		dst_name = os.path.join(dst_dir, name)
		shutil.move(src_name, dst_name)


def build_lib_setup():
	file_name = download_and_validate(DEFAULT_URL, MD5_DIGEST)
	if file_name is None:
		sys.exit(1)
	unpack_dir = unpack_file(file_name)
	move_files(PACK_FILE_ROOT_DIR, os.curdir, shutil.ignore_patterns('.git*'))
	shutil.rmtree(PACK_FILE_ROOT_DIR)
	os.remove(file_name)


if __name__ == '__main__':
	build_lib_setup()
