# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from ..event import EditSIPGeneralEvent


class TestEditSIPGeneralEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {}

    def test_marshal(self):
        command = EditSIPGeneralEvent()

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = EditSIPGeneralEvent.unmarshal(self.msg)

        self.assertEqual(command.name, EditSIPGeneralEvent.name)
