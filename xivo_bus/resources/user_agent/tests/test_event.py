# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import UserAgentConfigEvent


class ConcreteUserAgentConfigEvent(UserAgentConfigEvent):
    name = 'agent_event'


USER_UUID = 'abcd-1234'
AGENT_ID = 2


class TestUserAgentConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_uuid': USER_UUID,
            'agent_id': AGENT_ID,
        }

    def test_marshal(self):
        command = ConcreteUserAgentConfigEvent(USER_UUID, AGENT_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteUserAgentConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('user_uuid', USER_UUID),
            has_property('agent_id', AGENT_ID)))
