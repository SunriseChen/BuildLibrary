#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(
	name='STLport',
	version='5.2.1',

	author='Petr Ovtchenkov',
	author_email=' ',
	description='Multiplatform C++ Standard Library (STL implementation). Many compilers and operational environments supported. Standard (ISO/IEC 14882) compliance. Maximum efficiency. Exception and thread safety. Debug mode.',
	license='Other License',
	url='http://stlport.org',

	download_url='http://sourceforge.net/projects/stlport/files/STLport/STLport-5.2.1/STLport-5.2.1.tar.bz2',
)
