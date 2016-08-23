# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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
        return not(self == other)


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
