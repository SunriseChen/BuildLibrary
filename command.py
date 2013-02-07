#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import Command
from setuptools.command.install import install as _install
from distutils.errors import *


def validate_file_digest(dist, attr, value):
	digest_len = len(value)
	if digest_len != 32 and digest_len != 40:
		raise DistutilsSetupError('%r must be a md5 or sha1 digest value (got %r).' % (attr, value))


class download(Command):

	user_options = [
	]

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		print(self.distribution.file_digest)


class install(_install):

	user_options = _install.user_options + [
	]

	def initialize_options(self):
		_install.initialize_options(self)

	def finalize_options(self):
		_install.finalize_options(self)

	def run(self):
		self.run_command('download')
		_install.run(self)
