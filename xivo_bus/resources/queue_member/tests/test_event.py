# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest

from hamcrest import assert_that, equal_to, has_property, all_of

from xivo_bus.resources.queue_members.event import AgentQueueConfigEvent, AgentRemovedFromQueueEvent


AGENT_ID = 15
QUEUE_ID = 2
PENALTY = 5


class TestQueueMemberConfigEvent(unittest.TestCase):
    def setUp(self):
        self.msg = {
            'agent_id': AGENT_ID,
            'queue_id': QUEUE_ID,
            'penalty': PENALTY
        }

    def test_marshal(self):
        command = AgentQueueConfigEvent(QUEUE_ID, AGENT_ID, PENALTY)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = AgentQueueConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(has_property('agent_id', AGENT_ID),
                                  has_property('queue_id', QUEUE_ID),
                                  has_property('penalty', PENALTY)))


class TestAgentRemovedFromQueueEvent(unittest.TestCase):
    def setUp(self):
        self.msg = {
            'agent_id': AGENT_ID,
            'queue_id': QUEUE_ID,
        }

    def test_marshal(self):
        command = AgentRemovedFromQueueEvent(AGENT_ID, QUEUE_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = AgentRemovedFromQueueEvent.unmarshal(self.msg)

        assert_that(event, all_of(has_property('agent_id', AGENT_ID),
                                  has_property('queue_id', QUEUE_ID)))
