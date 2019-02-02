# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property


from ..event import LiveReloadEditedEvent


class TestLiveRealoadEditedEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'live_reload_enabled': True
        }

    def test_marshal(self):
        command = LiveReloadEditedEvent(True)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = LiveReloadEditedEvent.unmarshal(self.msg)

        assert_that(event, has_property('live_reload_enabled', True))
