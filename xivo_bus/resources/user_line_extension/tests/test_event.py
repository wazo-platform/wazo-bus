# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from ..event import UserLineExtensionConfigEvent


class ConcreteUserLineExtensionConfigEvent(UserLineExtensionConfigEvent):

    name = 'foo'

ID = 4221
USER_ID = 4321
LINE_ID = 9213
EXTENSION_ID = 54365
MAIN_USER = True
MAIN_LINE = True


class TestAbstractUserLineExtensionIDParams(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
            'user_id': USER_ID,
            'line_id': LINE_ID,
            'extension_id': EXTENSION_ID,
            'main_user': MAIN_USER,
            'main_line': MAIN_LINE
        }

    def test_marshal(self):
        command = ConcreteUserLineExtensionConfigEvent(ID, USER_ID, LINE_ID, EXTENSION_ID, MAIN_USER, MAIN_LINE)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteUserLineExtensionConfigEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteUserLineExtensionConfigEvent.name)
        self.assertEqual(command.id, ID)
        self.assertEqual(command.user_id, USER_ID)
        self.assertEqual(command.line_id, LINE_ID)
        self.assertEqual(command.extension_id, EXTENSION_ID)
        self.assertEqual(command.main_user, MAIN_USER)
        self.assertEqual(command.main_line, MAIN_LINE)
