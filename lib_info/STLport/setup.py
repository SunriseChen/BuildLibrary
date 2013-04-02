#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os


def add_msvc2010_support(base_dir):
	import re
	from common import modify_file

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


def pre_process():
	from common import Environment, clean_files

	print('Install STLport...')
	os.chdir('$basename')

	env = Environment()

	compiler = ''
	if env.platform.startswith('win'):
		if env.compiler == 'msvc':
			if float(env.compiler_version) > 9:
				compiler = 'msvc9'
				add_msvc2010_support(os.path.abspath(os.curdir))
			elif env.compiler_version[:3] == '7.1':
				compiler = 'msvc71'
			else:
				compiler = env.compiler + env.compiler_version[0]

	env.configure(compiler, '--with-static-rtl', '--with-dynamic-rtl')
	os.chdir('build/lib')
	env.make('clean', 'install')
	clean_files('obj')
	os.chdir('../../..')


def post_process():
	print('post process.')


def main():
	pre_process()

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

	post_process()


if __name__ == '__main__':
	main()
