#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

def get_abs_dir(directory):
	abs_dir = os.path.abspath(directory)
	if not os.path.exists(abs_dir):
		os.makedirs(abs_dir)
	return abs_dir

def download_file(url, target_dir):
	from urllib2 import urlopen, URLError, HTTPError

	# Open the url
	print('Opening url: ' + url)
	remote_file = urlopen(url)

	# Open our local file for writing
	print('Downloading...')
	file_name = os.path.basename(url)
	file_path = os.path.join(get_abs_dir(target_dir), file_name)
	with open(file_path, "wb") as local_file:
		local_file.write(remote_file.read())
	print('Downloaded.')

	return file_path


def unpack_file(file_name, target_dir):
	import tarfile

	print('Unpacking file: ' + file_name)
	dir_path = get_abs_dir(target_dir)
	if tarfile.is_tarfile(file_name):
		with tarfile.open(file_name) as tar_file:
			tar_file.extractall(dir_path)
	print('Unpacked.')

	return dir_path


def test():
	url = 'http://prdownloads.sourceforge.net/scons/scons-2.2.0.tar.gz'
	file_path = download_file(url, 'download')
	dir_path = unpack_file(file_path, 'unpack')
	print('Installing Scons...')
	dir_path = os.path.join(dir_path, os.path.basename(file_path)[:-7])
	os.chdir(dir_path)
	p = subprocess.Popen(['python', 'setup.py', 'install'])
	p.wait()
	if p.returncode == 0:
		print('Scons installed.')
	else:
		print('Scons install failed.')

def test1():
	from settings import PYTHON_HOME
	print(PYTHON_HOME)

if __name__ == '__main__':
	test()

