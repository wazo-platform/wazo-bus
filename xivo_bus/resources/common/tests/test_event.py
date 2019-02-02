# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from ..event import ResourceConfigEvent


class ConcreteResourceConfigEvent(ResourceConfigEvent):

    name = 'foo'


RESOURCE_ID = 42


class TestResourceConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {'id': RESOURCE_ID}

    def test_marshal(self):
        command = ConcreteResourceConfigEvent(RESOURCE_ID)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteResourceConfigEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteResourceConfigEvent.name)
        self.assertEqual(command.id, RESOURCE_ID)
