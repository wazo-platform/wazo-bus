# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserAgentConfigEvent(ResourceConfigEvent):

    def __init__(self, user_uuid, agent_id):
        self.user_uuid = user_uuid
        self.agent_id = agent_id

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'agent_id': self.agent_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_uuid'],
            msg['agent_id'])

    def __eq__(self, other):
        return (self.user_uuid == other.user_uuid and
                self.agent_id == other.agent_id)

    def __ne__(self, other):
        return not self == other


class UserAgentAssociatedEvent(UserAgentConfigEvent):
    name = 'agent_associated'

    def __init__(self, user_uuid, agent_id):
        super(UserAgentAssociatedEvent, self).__init__(user_uuid, agent_id)
        self.routing_key = 'config.users.{}.agents.updated'.format(self.user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)


class UserAgentDissociatedEvent(UserAgentConfigEvent):
    name = 'agent_dissociated'

    def __init__(self, user_uuid, agent_id):
        super(UserAgentDissociatedEvent, self).__init__(user_uuid, agent_id)
        self.routing_key = 'config.users.{}.agents.deleted'.format(self.user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)
