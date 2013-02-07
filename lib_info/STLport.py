#! /usr/bin/env python
# -*- coding: utf-8 -*-

from build import add_lib_info as _add_lib_info

def add_msvc2010_support():
	pass


def add_lib_info(lib_info):
	_add_lib_info(lib_info,
		name='STLport',
		version='5.2.1',

		entry_points={
			'distutils.commands': [
				'download = command:download',
				'install = command:install',
			],
			'distutils.setup_keywords': [
				'file_digest = command:validate_file_digest',
			],
		},

		author='Petr Ovtchenkov',
		author_email=' ',
		description='Multiplatform C++ Standard Library (STL implementation). Many compilers and operational environments supported. Standard (ISO/IEC 14882) compliance. Maximum efficiency. Exception and thread safety. Debug mode.',
		license='Other License',
		url='http://stlport.org',

		download_url='http://sourceforge.net/projects/stlport/files/STLport/STLport-5.2.1/STLport-5.2.1.tar.bz2',
		file_digest='a8341363e44d9d06a60e03215b38ddde',
		dependency_links=['http://sourceforge.net/projects/stlport/'],
	)
