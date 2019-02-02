# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest

from ..event import EditQueueGeneralEvent


class TestEditQueueGeneralEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {}

    def test_marshal(self):
        command = EditQueueGeneralEvent()

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = EditQueueGeneralEvent.unmarshal(self.msg)

        self.assertEqual(command.name, EditQueueGeneralEvent.name)
