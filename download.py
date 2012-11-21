#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

def download_file(url):
	from urllib2 import urlopen, URLError, HTTPError

	try:
		# Open the url
		print('Opening url: ' + url)
		remote_file = urlopen(url)

		# Open our local file for writing
		print('Downloading...')
		file_name = os.path.basename(url)
		with open(file_name, "wb") as local_file:
			local_file.write(remote_file.read())
		print('Downloaded.')

		return file_name

	# handle errors
	except HTTPError, e:
		print('HTTP Error: %s %s' % (e.code, url))
	except URLError, e:
		print('URL Error: %s %s' % (e.reason, url))


def unpack_file(file_name):
	import tarfile
	print('Unpacking file: ' + file_name)
	tar = tarfile.open(file_name)
	tar.extractall()
	tar.close()
	print('Unpacked.')


def test():
	url = 'http://prdownloads.sourceforge.net/scons/scons-2.2.0.tar.gz'
	file_name = download_file(url)
	unpack_file(file_name)

if __name__ == '__main__':
	test()

