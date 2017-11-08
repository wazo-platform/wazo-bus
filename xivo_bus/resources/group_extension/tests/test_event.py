# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique Inc.
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import GroupExtensionConfigEvent


class ConcreteGroupExtensionConfigEvent(GroupExtensionConfigEvent):
    name = 'trunk_endpoint_event'


INCALL_ID = 1
EXTENSION_ID = 2


class TestGroupExtensionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'group_id': INCALL_ID,
            'extension_id': EXTENSION_ID,
        }

    def test_marshal(self):
        command = ConcreteGroupExtensionConfigEvent(INCALL_ID, EXTENSION_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteGroupExtensionConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('group_id', INCALL_ID),
            has_property('extension_id', EXTENSION_ID)))
