#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
公共代码。
'''

# pylint: disable=C0325

import os
import re
import shutil
import subprocess
import sys
import tempfile
from distutils import ccompiler
from distutils.errors import *
from distutils.version import StrictVersion
from string import Template

from pkg_resources import *

from SCons.Environment import Environment as _Environment


def _args_to_list(args):
    lst = []
    if args:
        for arg in args:
            if isinstance(arg, list):
                lst += arg
            else:
                lst.append(arg)

    return lst


def modify_file(filename, modify_list):
    '''modify_file'''
    if not os.path.isfile(filename):
        return

    text = ''
    with open(filename) as input_file:
        text = input_file.read()

    for item in modify_list or []:
        text = item[0].sub(item[1], text)

    with tempfile.NamedTemporaryFile('w', delete=False) as output_file:
        output_file.write(text)

    shutil.move(output_file.name, filename)


def clean_files(*args):
    '''clean_files'''
    import glob

    for path in _args_to_list(args):
        if glob.has_magic(path):
            clean_files(glob.glob(path))
        elif os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def get_project_name(lib_info_dir, spec):
    '''get_project_name'''
    for name in os.listdir(lib_info_dir):
        if spec.lower() == name.lower() and os.path.isdir(os.path.join(lib_info_dir, name)):
            return name

    return spec


def get_lib_name(name, version):
    '''get_lib_name'''
    return '%s-%s' % (name, version)


def get_dist(req, env, source, develop_ok):
    '''get_dist'''
    for dist in env[req.key]:
        if dist.precedence == DEVELOP_DIST and not develop_ok:
            continue

        if dist in req and (dist.precedence <= SOURCE_DIST or not source):
            return dist

    raise DistutilsError("Can't get %r" % req)


def generate_setup(lib_info_dir, project_name, version, setup_base):
    '''generate_setup'''
    src_file = os.path.join(lib_info_dir, project_name, 'setup.py')
    setup_script = os.path.join(setup_base, 'setup.py')
    print('Writing %s' % setup_script)
    with open(setup_script, 'w') as dst:
        with open(src_file) as src:
            for line in src:
                line = Template(line).safe_substitute(
                    name=project_name,
                    version=version,
                    lib_name=get_lib_name(project_name, version),
                )
                dst.write(line)

    return setup_script


class Environment(object):
    '''Environment'''

    def __init__(self):
        env = _Environment()
        self.arch = env['TARGET_ARCH']
        self.platform = sys.platform
        self.compiler = ccompiler.get_default_compiler()
        self.compiler_version = StrictVersion('0.0')
        if self.compiler == 'msvc':
            self.compiler_version = StrictVersion(env['MSVC_VERSION'])
            os.environ['PATH'] = env['ENV']['PATH']
            os.environ['INCLUDE'] = env['ENV']['INCLUDE']
            os.environ['LIB'] = env['ENV']['LIB']
            os.environ['LIBPATH'] = env['ENV']['LIBPATH']


    def configure(self, *args):
        '''configure'''
        cmd = ['./configure']
        if self.platform.startswith('win'):
            cmd[0] = 'configure.bat'
        elif not os.path.exists(cmd[0]):
            cmd[0] = './configure.sh'

        if os.path.exists(cmd[0]):
            cmd += _args_to_list(args)
        else:
            cmd = _args_to_list(args)

        return subprocess.call(cmd) if cmd else False


    def make(self, *args):
        '''make'''
        cmd = ['make']
        if self.compiler == 'msvc':
            cmd[0] = 'nmake'

        cmd += _args_to_list(args)

        return subprocess.call(cmd) if cmd else False


def generate_settings(project_name, import_dir, include_path, library_path):
    '''generate_settings'''
    settings_filename = os.path.join(import_dir, 'local_settings.py')
    if not os.path.exists(settings_filename):
        with open(settings_filename, 'w') as settings_file:
            settings_file.write('''#! /usr/bin/env python
# -*- coding: utf-8 -*-

include_path = [
]

library_path = [
]
''')

    def modify_path(match, path):
        '''modify_path'''
        curr_path = re.match(r'^[\'"](.*)[\'"]\s*,$', match.group(2), flags=re.M | re.S)
        if curr_path:
            curr_path = re.split(r'[\'"]\s*,\s*[\'"]', curr_path.group(1), flags=re.M)
        else:
            curr_path = []
        tag = '%s\\%s-' % (project_name, project_name)
        path = [p for p in curr_path if tag not in p] + path
        return "%s\n\t'%s',\n]" % (match.group(1), "',\n\t'".join(path))

    modify_list = []
    if include_path:
        modify_list.append(
            (re.compile(r'^(include_path\s*=\s*\[)\s*(.*?)\s*\]$', re.M | re.S),
             lambda m: modify_path(m, include_path)))
    if library_path:
        modify_list.append(
            (re.compile(r'^(library_path\s*=\s*\[)\s*(.*?)\s*\]$', re.M | re.S),
             lambda m: modify_path(m, library_path)))
    modify_file(settings_file, modify_list)


def generate_props(lib_info_dir, project_name, import_dir, include_path, library_path):
    '''generate_props'''
    from xmltools import get_namespace, namespace_path
    from xml.etree import ElementTree as etree

    props_file = os.path.join(import_dir, 'Library.props')
    if not os.path.exists(props_file):
        sample_file = os.path.join(lib_info_dir, 'Library.props.sample')
        shutil.copy(sample_file, props_file)

    tree = etree.ElementTree()
    root = tree.parse(props_file)
    uri = get_namespace(root)
    etree.register_namespace('', uri)
    include = root.find(namespace_path(uri, 'PropertyGroup/IncludePath'))
    library = root.find(namespace_path(uri, 'PropertyGroup/LibraryPath'))

    def modify_path(element, path, path_macro):
        '''modify_path'''
        if element is not None:
            curr_path = element.text.split(';')
            tag = '%s\\%s-' % (project_name, project_name)
            path = [
                p for p in curr_path if (p != path_macro and tag not in p)
            ] + path
            path.append(path_macro)
            element.text = ';'.join(path)

    modify_path(include, include_path, '$(IncludePath)')
    modify_path(library, library_path, '$(LibraryPath)')

    tree.write(props_file, 'utf-8', True)


def generate_import(lib_info_dir, project_name, version, base_dir):
    '''generate_import'''
    lib_dir = os.path.join(base_dir, project_name, get_lib_name(project_name, version))
    import_dir = os.path.join(base_dir, 'Import')

    env = Environment()
    if env.platform == 'win32':
        import ntfslink

        import_link = os.path.join(import_dir, project_name)

        if os.path.exists(import_link):
            if os.path.isfile(import_link):
                os.remove(import_link)
            elif os.path.islink(import_link):
                os.rmdir(import_link)
            else:
                shutil.rmtree(import_link)
        else:
            ensure_directory(import_link)

        os.symlink(lib_dir, import_link)

    include_path = os.getenv('INCLUDE_PATH', '').split(os.pathsep)
    library_path = os.getenv('LIBRARY_PATH', '').split(os.pathsep)

    if include_path or library_path:
        def _abspath(path):
            return os.path.abspath(os.path.join(lib_dir, path))

        include_path = map(_abspath, include_path)
        library_path = map(_abspath, library_path)

        generate_settings(project_name, import_dir, include_path, library_path)

        if env.compiler == 'msvc':
            generate_props(lib_info_dir, project_name, import_dir, include_path, library_path)


def test():
    '''测试'''
    print('Test passed !')


if __name__ == '__main__':
    test()
