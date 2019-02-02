# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from ..event import SipEndpointConfigEvent

ID = 42


class ConcreteSipEndpointConfigEvent(SipEndpointConfigEvent):

    name = 'foo'


class TestAbstractSipEndpointIDParams(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
        }

    def test_marshal(self):
        command = ConcreteSipEndpointConfigEvent(ID)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteSipEndpointConfigEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteSipEndpointConfigEvent.name)
        self.assertEqual(command.id, ID)
