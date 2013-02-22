#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, tempfile, shutil, re


def modify_file(filename, modify_list):
	text = ''
	with open(filename) as f:
		text = f.read()

	for m in modify_list or []:
		if m[1] not in text:
			text = m[0].sub(m[1], text)

	f = tempfile.NamedTemporaryFile('a', delete=False)
	f.write(text)
	f.close()

	shutil.move(f.name, filename)


def add_msvc2010_support(base_dir):
	modify_list = [
		(re.compile(r'^inline\s+_STLP_LONG_LONG\s+abs\(_STLP_LONG_LONG\s+__x\)\s+\{\s+return\s+__x\s+<\s+0\s+\?\s+-__x\s+:\s+__x;\s+\}$', re.M),
		'''#    if !defined(_STLP_MSVC) || (_STLP_MSVC < 1600)
inline _STLP_LONG_LONG  abs(_STLP_LONG_LONG __x) { return __x < 0 ? -__x : __x; }
#    endif'''),
	]
	cstdlib = os.path.join(base_dir, 'stlport/stl/_cstdlib.h')
	modify_file(cstdlib, modify_list)


def pre_process():
	print('pre process.')
	print('I\'m STLport.')


def post_process():
	print('post process.')


def main():
	pre_process()

	from setuptools import setup
	setup(
		name='STLport',
		version='$version',

		author='Petr Ovtchenkov',
		author_email=' ',
		description='Multiplatform C++ Standard Library (STL implementation). Many compilers and operational environments supported. Standard (ISO/IEC 14882) compliance. Maximum efficiency. Exception and thread safety. Debug mode.',
		license='Other License',
		url='http://stlport.org',
	)

	post_process()


if __name__ == '__main__':
	main()
	#add_msvc2010_support('../../../STLport/STLport-5.2.1')
