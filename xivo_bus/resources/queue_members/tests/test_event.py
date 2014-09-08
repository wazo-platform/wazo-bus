# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

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
