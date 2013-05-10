#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as etree


if etree.VERSION[0:3] == '1.2':
	#in etree < 1.3, this is a workaround for supressing prefixes

	def fixtag(tag, namespaces):
		import string
		# given a decorated tag (of the form {uri}tag), return prefixed
		# tag and namespace declaration, if any
		if isinstance(tag, etree.QName):
			tag = tag.text
		namespace_uri, tag = string.split(tag[1:], "}", 1)
		prefix = namespaces.get(namespace_uri)
		if namespace_uri not in namespaces:
			prefix = etree._namespace_map.get(namespace_uri)
			if namespace_uri not in etree._namespace_map:
				prefix = "ns%d" % len(namespaces)
			namespaces[namespace_uri] = prefix
			if prefix == "xml":
				xmlns = None
			else:
				if prefix is not None:
					nsprefix = ':' + prefix
				else:
					nsprefix = ''
				xmlns = ("xmlns%s" % nsprefix, namespace_uri)
		else:
			xmlns = None
		if prefix is not None:
			prefix += ":"
		else:
			prefix = ''

		return "%s%s" % (prefix, tag), xmlns

	def register_namespace(prefix, uri):
		etree._namespace_map[uri] = None if prefix == '' else prefix

	etree.fixtag = fixtag
	etree.register_namespace = register_namespace


def test():
	something = etree.Element('{http://some.namespace}token')
	result = etree.tostring(something)
	assert result == '<ns0:token xmlns:ns0="http://some.namespace" />', result
	etree.register_namespace('', 'http://some.namespace')
	result = etree.tostring(something)
	assert result == '<token xmlns="http://some.namespace" />', result
	print('Test passed !')


if __name__ == '__main__':
	test()
