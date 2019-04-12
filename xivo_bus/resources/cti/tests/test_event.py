# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
import uuid

from hamcrest import assert_that
from hamcrest import equal_to

from ..event import AgentStatusUpdateEvent

SOME_UUID = str(uuid.uuid4())


class TestAgentStatusUpdateEvent(unittest.TestCase):

    def test_marshal(self):
        agent_id = 42
        status = 'logged_in'

        event = AgentStatusUpdateEvent(agent_id, status)
        msg = event.marshal()

        assert_that(msg, equal_to({'agent_id': 42,
                                   'status': 'logged_in'}))

    def test_that_string_ids_are_not_leaked(self):
        agent_id = '42'
        status = 'logged_in'

        event = AgentStatusUpdateEvent(agent_id, status)
        msg = event.marshal()

        assert_that(msg, equal_to({'agent_id': 42,
                                   'status': 'logged_in'}))
