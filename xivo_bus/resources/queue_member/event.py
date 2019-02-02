# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class QueueMemberAgentAssociatedEvent(object):
    name = 'agent_queue_associated'
    routing_key = 'config.agent_queue_association.created'

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
        return (self.queue_id == other.queue_id
                and self.agent_id == other.agent_id
                and self.penalty == other.penalty)

    def __ne__(self, other):
        return not self == other


class QueueMemberAgentDissociatedEvent(object):
    name = "agent_removed_from_queue"
    routing_key = 'config.agent_queue_association.deleted'

    def __init__(self, queue_id, agent_id):
        self.queue_id = queue_id
        self.agent_id = agent_id

    def marshal(self):
        return {
            'queue_id': self.queue_id,
            'agent_id': self.agent_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['queue_id'], msg['agent_id'])

    def __eq__(self, other):
        return (self.queue_id == other.queue_id
                and self.agent_id == other.agent_id)

    def __ne__(self, other):
        return not self == other


class QueueMemberUserConfigEvent(object):

    def __init__(self, queue_id, user_uuid):
        self.queue_id = queue_id
        self.user_uuid = user_uuid

    def marshal(self):
        return {
            'queue_id': self.queue_id,
            'user_uuid': self.user_uuid,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['queue_id'], msg['user_uuid'])

    def __eq__(self, other):
        return (self.queue_id == other.queue_id
                and self.user_uuid == other.user_uuid)

    def __ne__(self, other):
        return not self == other


class QueueMemberUserAssociatedEvent(QueueMemberUserConfigEvent):
    name = 'user_queue_associated'
    routing_key = 'config.user_queue_association.created'


class QueueMemberUserDissociatedEvent(QueueMemberUserConfigEvent):
    name = "user_removed_from_queue"
    routing_key = 'config.user_queue_association.deleted'
