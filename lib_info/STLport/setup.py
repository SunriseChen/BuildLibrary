#! /usr/bin/env python
# -*- coding: utf-8 -*-


def say_hello():
	print('hello world!')


def add_msvc2010_support():
	pass


def main():
	say_hello()

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


if __name__ == '__main__':
	main()
