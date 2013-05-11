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


def get_namespace(element):
	return element.tag[1:].split('}')[0] if element.tag.startswith('{') else ''


def namespace_tag(uri, tag):
	return etree.QName(uri, tag).text if uri else tag


def namespace_path(uri, path):
	if uri:
		tags = path.split('/')
		return '/'.join(map(lambda tag: namespace_tag(uri, tag), tags))

	return path


def test():
	uri = 'http://some.namespace'
	something = etree.Element('{%s}token' % uri)
	result = etree.tostring(something)
	assert result == '<ns0:token xmlns:ns0="%s" />' % uri, result
	etree.register_namespace('', uri)
	result = etree.tostring(something)
	assert result == '<token xmlns="%s" />' % uri, result
	result = namespace_tag(uri, 'tag')
	assert result == '{%s}tag' % uri, result
	result = namespace_path(uri, 'a/b/c')
	assert result == '{%s}a/{%s}b/{%s}c' % (uri, uri, uri), result
	print('Test passed !')


if __name__ == '__main__':
	test()
