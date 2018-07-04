# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest

from hamcrest import (
    assert_that,
    equal_to,
    has_properties,
)

from ..event import (
    QueueMemberAgentAssociatedEvent,
    QueueMemberAgentDissociatedEvent,
    QueueMemberUserConfigEvent,
)

USER_UUID = '1234-abcd'
AGENT_ID = 15
QUEUE_ID = 2
PENALTY = 5


class TestQueueMemberAssociateEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'agent_id': AGENT_ID,
            'queue_id': QUEUE_ID,
            'penalty': PENALTY
        }

    def test_marshal(self):
        command = QueueMemberAgentAssociatedEvent(QUEUE_ID, AGENT_ID, PENALTY)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = QueueMemberAgentAssociatedEvent.unmarshal(self.msg)

        assert_that(event, has_properties(
            agent_id=AGENT_ID,
            queue_id=QUEUE_ID,
            penalty=PENALTY,
        ))


class TestQueueMemberDissociateEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'agent_id': AGENT_ID,
            'queue_id': QUEUE_ID,
        }

    def test_marshal(self):
        command = QueueMemberAgentDissociatedEvent(QUEUE_ID, AGENT_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = QueueMemberAgentDissociatedEvent.unmarshal(self.msg)

        assert_that(event, has_properties(
            agent_id=AGENT_ID,
            queue_id=QUEUE_ID,
        ))


class TestQueueMemberConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_uuid': USER_UUID,
            'queue_id': QUEUE_ID,
        }

    def test_marshal(self):
        command = QueueMemberUserConfigEvent(QUEUE_ID, USER_UUID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = QueueMemberUserConfigEvent.unmarshal(self.msg)

        assert_that(event, has_properties(
            user_uuid=USER_UUID,
            queue_id=QUEUE_ID,
        ))
