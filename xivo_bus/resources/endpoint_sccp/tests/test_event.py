# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from ..event import SccpEndpointConfigEvent

ID = 42


class ConcreteSccpEndpointConfigEvent(SccpEndpointConfigEvent):

    name = 'foo'


class TestAbstractSccpEndpointIDParams(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
        }

    def test_marshal(self):
        command = ConcreteSccpEndpointConfigEvent(ID)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteSccpEndpointConfigEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteSccpEndpointConfigEvent.name)
        self.assertEqual(command.id, ID)
