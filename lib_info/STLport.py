#! /usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.dist import Distribution


class LibraryDistribution(Distribution):

	#def parse_config_files(self):
	#	Distribution.parse_config_files(self)

	#def parse_command_line(self):
	#	return Distribution.parse_command_line(self)

	def get_command_class(self, command):
		klass = Distribution.get_command_class(self, command)
		#print('klass = ')
		#print(klass)
		return klass

	def get_command_obj(self, command, create=1):
		cmd_obj = Distribution.get_command_obj(self, command, create)
		#print('cmd_obj =')
		#print(cmd_obj)
		return cmd_obj


setup(
		name='STLport',
		version='5.2.1',
		#scripts=['.py'],

		author='Petr Ovtchenkov',
		author_email='',
		description='Multiplatform C++ Standard Library (STL implementation). Many compilers and operational environments supported. Standard (ISO/IEC 14882) compliance. Maximum efficiency. Exception and thread safety. Debug mode.',
		license='Other License',
		keywords='',
		url='http://stlport.org',

		download_url='http://sourceforge.net/projects/stlport/files/latest/download',
		distclass=LibraryDistribution,
		)

