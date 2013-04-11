#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
from common import *


def add_msvc2010_support(base_dir):
	filename = os.path.join(base_dir, 'stlport/stl/_cstdlib.h')
	modify_list = [
		(re.compile(r'^inline\s+_STLP_LONG_LONG\s+abs\(_STLP_LONG_LONG\s+__x\)\s+\{\s+return\s+__x\s+<\s+0\s+\?\s+-__x\s+:\s+__x;\s+\}$', re.M),
		'''#    if !defined(_STLP_MSVC) || (_STLP_MSVC < 1600)
inline _STLP_LONG_LONG  abs(_STLP_LONG_LONG __x) { return __x < 0 ? -__x : __x; }
#    endif'''),
	]
	modify_file(filename, modify_list)

	filename = os.path.join(base_dir, 'stlport/stl/type_traits.h')
	modify_list = [
		(re.compile(r'^#endif\s+/\*\s+_STLP_USE_BOOST_SUPPORT\s+\*/$', re.M),
		'''#  include <boost/type_traits/remove_const.hpp>
#endif /* _STLP_USE_BOOST_SUPPORT */'''),
	]
	modify_file(filename, modify_list)


def fix_stlport6(base_dir):
	filename = os.path.join(base_dir, 'stlport/stl/config/_msvc.h')
	modify_list = [
		(re.compile(r'^#\s+define\s+_STLP_DONT_USE_BOOL_TYPEDEF\s+1\s+#\s+endif$', re.M),
		'''#    define _STLP_DONT_USE_BOOL_TYPEDEF 1
//#  endif	// fix bug'''),
	]
	modify_file(filename, modify_list)


def build(version):
	print('Install STLport...')

	base_dir = os.path.abspath(os.curdir)
	config_parameter = []

	env = Environment()
	if env.compiler == 'msvc':
		if env.compiler_version > '9.0':
			config_parameter.append('msvc9')
			add_msvc2010_support(base_dir)
		elif '7.0' < env.compiler_version and env.compiler_version < '7.2':
			config_parameter.append('msvc71')
		else:
			config_parameter.append('msvc' + env.compiler_version[0])

	config_parameter += ['--with-static-rtl', '--with-dynamic-rtl']
	#env.configure(config_parameter)

	if version > '5.2.1':
		fix_stlport6(base_dir)
		os.chdir('src')
	else:
		os.chdir('build/lib')
	#env.make('install')

	clean_files('obj')
	if version > '5.2.1':
		os.chdir('..')
	else:
		os.chdir('../..')

	return True


def main():
	from distutils.version import LooseVersion

	version = LooseVersion('$version')
	os.chdir('$basename')
	if build(version):
		os.chdir('..')

		from setuptools import setup
		setup(
			name='STLport',
			version='$version',

			author='Petr Ovtchenkov',
			author_email='support@stlport.com',
			description='Multiplatform C++ Standard Library (STL implementation). Many compilers and operational environments supported. Standard (ISO/IEC 14882) compliance. Maximum efficiency. Exception and thread safety. Debug mode.',
			license='Other License',
			url='http://stlport.org',
		)
	else:
		sys.exit(1)


if __name__ == '__main__':
	main()
