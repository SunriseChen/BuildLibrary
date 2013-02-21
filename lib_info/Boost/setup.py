#! /usr/bin/env python
# -*- coding: utf-8 -*-


def say_hello():
	print('hello world!\nI\'m Boost.')


def add_msvc2010_support():
	pass


def main():
	say_hello()

	from setuptools import setup
	setup(
		name='Boost',
		version='$version',

		author='Boost',
		author_email=' ',
		description='Boost provides free portable peer-reviewed C++ libraries. The emphasis is on portable libraries which work well with the C++ Standard Library. See http://www.boost.org',
		license='Boost Software License',
		url='http://www.boost.org',
	)


if __name__ == '__main__':
	main()
