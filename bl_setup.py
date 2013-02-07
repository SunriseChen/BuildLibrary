#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, shutil

DEFAULT_VERSION = '0.1.0'
DEFAULT_URL     = 'https://github.com/SunriseChen/BuildLibrary/archive/master.zip'
FILE_DIGEST = None
PACK_FILE_ROOT_DIR = 'BuildLibrary-master'

SETUPTOOLS_URL = 'http://peak.telecommunity.com/dist/ez_setup.py'


def download_file(url, target_dir=os.curdir):
	from urllib2 import urlopen, URLError, HTTPError

	print('Downloading url: ' + url)
	remote_file = urlopen(url)

	if not os.path.exists(target_dir):
		os.makedirs(target_dir)
	file_name = os.path.basename(url)
	file_path = os.path.join(target_dir, file_name)
	with open(file_path, 'wb') as local_file:
		local_file.write(remote_file.read())

	remote_file.close()
	print('Downloaded.')

	return os.path.realpath(file_path)


def get_md5(data):
	hash_data = None
	try:
		# Python version >= 2.5
		from hashlib import md5
	except ImportError:
		# Python version < 2.5
		from md5 import md5
	hash_data = md5(data)

	return hash_data


def get_sha1(data):
	hash_data = None
	try:
		# Python version >= 2.5
		import hashlib
		hash_data = hashlib.sha1(data)
	except ImportError:
		# Python version < 2.5
		import sha
		hash_data = sha.new(data)

	return hash_data


def validate_file(file_name, file_digest):
	if file_digest is None:
		return True

	with open(file_name, 'rb') as file_data:
		digest_len = len(file_digest)
		hash_data = None
		if digest_len == 32:
			hash_data = get_md5(file_data.read())
		elif digest_len == 40:
			hash_data = get_sha1(file_data.read())
		if hash_data:
			print(file_digest)
			print(hash_data.hexdigest())
			return (file_digest == hash_data.hexdigest())

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
		zip_file = zipfile.ZipFile(file_name)
		zip_file.extractall(target_dir)
		zip_file.close()
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
	file_name = download_and_validate(DEFAULT_URL, FILE_DIGEST)
	if file_name is None:
		sys.exit(1)
	unpack_dir = unpack_file(file_name)
	move_files(PACK_FILE_ROOT_DIR, os.curdir, shutil.ignore_patterns('.git*'))
	shutil.rmtree(PACK_FILE_ROOT_DIR)
	os.remove(file_name)

	setuptools = download_file(SETUPTOOLS_URL)
	import ez_setup
	ez_setup.use_setuptools()

	import subprocess
	subprocess.call(['easy_install', 'scons'])


if __name__ == '__main__':
	build_lib_setup()
