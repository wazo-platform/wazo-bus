#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages


setup(
    name='xivo-bus',
    version='0.1',
    description='XiVO BUS libraries',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='http://wazo.community',
    license='GPLv3',
    packages=find_packages(),
)
