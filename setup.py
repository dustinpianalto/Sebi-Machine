#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Setup.
"""
import re
from setuptools import setup
import traceback


package_name = 'sebimachine'


req_line_test = lambda l: l and l[0] != '#'


with open('README.md') as fp:
    readme = fp.read()


with open('requirements.txt') as fp:
    requirements = {*filter(req_line_test, map(str.lstrip, fp.read().split('\n')))}


with open(f'{package_name}/__init__.py') as fp:
    attrs = {}
    print('Attributes:')
    for k, v in re.findall(r'^__(\w+)__\s?=\s?"([^"]*)"', fp.read(), re.M):
        k = 'name' if k == 'title' else k
        attrs[k] = v
        print(k, v)


# Use pip on invoke to install requirements. Ensures we can essentially just run this
# script without setuptools arguments. TODO: fix.
try:
    import pip
    pip.main(['install', *install_requires])
except (ModuleNotFoundError, ImportError):
    print('Failed to import pip. Install git dependencies manually.')
    traceback.print_exc()


setup(
    long_description=readme,
    **attrs
)
