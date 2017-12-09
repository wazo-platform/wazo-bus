# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from ..event import EditIAXCallNumberLimitsEvent


class TestEditIAXCallNumberLimitsEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {}

    def test_marshal(self):
        command = EditIAXCallNumberLimitsEvent()

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = EditIAXCallNumberLimitsEvent.unmarshal(self.msg)

        self.assertEqual(command.name, EditIAXCallNumberLimitsEvent.name)
