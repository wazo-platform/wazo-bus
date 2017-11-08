# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from ..event import CustomEndpointConfigEvent

ID = 42
INTERFACE = 'dahdi/i1'


class ConcreteCustomEndpointConfigEvent(CustomEndpointConfigEvent):

    name = 'foo'


class TestAbstractCustomEndpointIDParams(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
            'interface': INTERFACE,
        }

    def test_marshal(self):
        command = ConcreteCustomEndpointConfigEvent(ID, INTERFACE)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteCustomEndpointConfigEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteCustomEndpointConfigEvent.name)
        self.assertEqual(command.id, ID)
        self.assertEqual(command.interface, INTERFACE)
