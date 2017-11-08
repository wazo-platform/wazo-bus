# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class AgentQueueConfigEvent(object):
    routing_key = 'config.agent_queue_association.{}'

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

    def __eq__(self, other):
        return (self.queue_id == other.queue_id and
                self.agent_id == other.agent_id and
                self.penalty == other.penalty)

    def __ne__(self, other):
        return not self == other


class AgentQueueAssociationEditedEvent(AgentQueueConfigEvent):
    name = 'agent_queue_association_edited'
    routing_key = AgentQueueConfigEvent.routing_key.format('edited')


class AgentQueueAssociatedEvent(AgentQueueConfigEvent):
    name = 'agent_queue_associated'
    routing_key = AgentQueueConfigEvent.routing_key.format('created')


class AgentRemovedFromQueueEvent(AgentQueueConfigEvent):
    name = "agent_removed_from_queue"
    routing_key = AgentQueueConfigEvent.routing_key.format('deleted')

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

    def __eq__(self, other):
        return (self.queue_id == other.queue_id and
                self.agent_id == other.agent_id)

    def __ne__(self, other):
        return not self == other
