# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import LineExtensionConfigEvent


class ConcreteLineExtensionConfigEvent(LineExtensionConfigEvent):
    name = 'line_extension_event'


LINE_ID = 1
EXTENSION_ID = 2


class TestLineExtensionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'line_id': LINE_ID,
            'extension_id': EXTENSION_ID,
        }

    def test_marshal(self):
        command = ConcreteLineExtensionConfigEvent(LINE_ID, EXTENSION_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteLineExtensionConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('line_id', LINE_ID),
            has_property('extension_id', EXTENSION_ID)))
