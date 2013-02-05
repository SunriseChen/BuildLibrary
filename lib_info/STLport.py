#! /usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.dist import Distribution


def get_dist_list():
	dist_list = []

	lib_info = {
		'name': 'STLport',
		'version': '5.2.1',
		'author': 'Petr Ovtchenkov',
		'author_email': '',
		'description': 'Multiplatform C++ Standard Library (STL implementation). Many compilers and operational environments supported. Standard (ISO/IEC 14882) compliance. Maximum efficiency. Exception and thread safety. Debug mode.',
		'license': 'Other License',
		'keywords': '',
		'url': 'http://stlport.org',

		'download_url': 'http://sourceforge.net/projects/stlport/files/latest/download',
	}
	dist_list.append(Distribution(lib_info))

	return dist_list
