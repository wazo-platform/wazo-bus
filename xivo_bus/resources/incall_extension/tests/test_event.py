# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import IncallExtensionConfigEvent


class ConcreteIncallExtensionConfigEvent(IncallExtensionConfigEvent):
    name = 'trunk_endpoint_event'


INCALL_ID = 1
EXTENSION_ID = 2


class TestIncallExtensionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'incall_id': INCALL_ID,
            'extension_id': EXTENSION_ID,
        }

    def test_marshal(self):
        command = ConcreteIncallExtensionConfigEvent(INCALL_ID, EXTENSION_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteIncallExtensionConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('incall_id', INCALL_ID),
            has_property('extension_id', EXTENSION_ID)))
