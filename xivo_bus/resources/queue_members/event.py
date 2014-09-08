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

from xivo_bus.resources.common.event import ResourceConfigEvent


class AgentQueueConfigEvent(ResourceConfigEvent):
    def __init__(self, queue_id, agent_id, penalty):
        self.queue_id = queue_id
        self.agent_id = agent_id
        self.penalty = penalty

    def marshal(self):
        return {
            'queue_id': self.queue_id,
            'agent_id': self.agent_id,
            'penalty': self.penalty
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['queue_id'], msg['agent_id'], msg['penalty'])


class AgentQueueAssociationEditedEvent(AgentQueueConfigEvent):
    name = 'agent_queue_association_edited'


class AgentQueueAssociatedEvent(AgentQueueConfigEvent):
    name = 'agent_queue_associated'


class AgentRemovedFromQueueEvent(AgentQueueConfigEvent):
    name = "agent_removed_from_queue"

    def __init__(self, agent_id, queue_id):
        self.queue_id = queue_id
        self.agent_id = agent_id

    def marshal(self):
        return {
            'queue_id': self.queue_id,
            'agent_id': self.agent_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['agent_id'], msg['queue_id'])
