# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from mock import sentinel
from ..event import AMIEvent


class TestAMIEvent(unittest.TestCase):

    def test_marshal(self):
        event = AMIEvent(sentinel.name, sentinel.variables)

        result = event.marshal()

        self.assertEqual(result, sentinel.variables)

    def test_string_name(self):
        event = AMIEvent(sentinel.name, sentinel.variables)

        self.assertEqual(event.name, sentinel.name)
