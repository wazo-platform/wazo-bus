#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup

setup(
    name='xivo-bus',
    version='0.1',
    description='XiVO BUS libraries',
    author='Avencall',
    author_email='dev@avencall.com',
    url='http://git.xivo.fr/',
    license='GPLv3',
    packages=['xivo_bus',
              'xivo_bus.ctl',
              'xivo_bus.ressource',
              'xivo_bus.ressource.agent',
              'xivo_bus.ressource.agent.command',
              'xivo_bus.ressource.xivo',
              'xivo_bus.ressource.xivo.command', ]
)
