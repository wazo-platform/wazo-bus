# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup

setup(
    name='bus-test',
    version='0.1',
    packages=['bus_test'],
    include_package_data=True,
    install_requires=[
        'flask', 'kombu'
    ],
)
