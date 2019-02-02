# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from ..event import DeviceConfigEvent

ID = 'abcd1234'


class ConcreteDeviceEvent(DeviceConfigEvent):
    name = 'device_concrete_event'


class TestDeviceConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
        }

    def test_marshal(self):
        event = ConcreteDeviceEvent(ID)

        msg = event.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        event = ConcreteDeviceEvent.unmarshal(self.msg)

        self.assertEqual(event.name, ConcreteDeviceEvent.name)
        self.assertEqual(event.id, ID)
