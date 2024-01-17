#!/usr/bin/env python3
# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import find_packages, setup

setup(
    name='wazo-bus',
    version='0.2',
    description='Wazo bus library',
    install_requires=["kombu==5.0.2", "typing_extensions==4.4.0"],
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='http://wazo.community',
    license='GPLv3',
    packages=find_packages(),
)
