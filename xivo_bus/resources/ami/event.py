# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class AMIEvent(object):

    def __init__(self, name, variables):
        self.name = name
        self.variables = variables
        self.routing_key = 'ami.{}'.format(self.name)

    def marshal(self):
        return self.variables
