# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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


class EditUserEvent(ResourceConfigEvent):
    name = 'user_edited'
    routing_key = 'config.user.edited'


class CreateUserEvent(ResourceConfigEvent):
    name = 'user_created'
    routing_key = 'config.user.created'


class DeleteUserEvent(ResourceConfigEvent):
    name = 'user_deleted'
    routing_key = 'config.user.deleted'


class _BaseConfigUserEvent(object):
    def __init__(self, resource_uuid):
        self.uuid = resource_uuid

    def marshal(self):
        return {'uuid': self.uuid}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['uuid'])

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __ne__(self, other):
        return not self == other


class EditUserServiceEvent(_BaseConfigUserEvent):
    def __init__(self, resource_uuid, service_name, service_enabled):
        super(EditUserServiceEvent, self).__init__(resource_uuid)
        self.service_enabled = service_enabled
        self.name = 'users_services_{}_updated'.format(service_name)
        self.routing_key = 'config.users.{}.services.{}.updated'.format(resource_uuid, service_name)
        self.required_acl = 'events.{}'.format(self.routing_key)

    def marshal(self):
        return {
            'uuid': self.uuid,
            'enabled': self.service_enabled
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['uuid'],
                   msg['enabled'])


class EditUserForwardEvent(_BaseConfigUserEvent):
    def __init__(self, resource_uuid, forward_name, forward_enabled, forward_destination):
        super(EditUserForwardEvent, self).__init__(resource_uuid)
        self.forward_enabled = forward_enabled
        self.forward_destination = forward_destination
        self.name = 'users_forwards_{}_updated'.format(forward_name)
        self.routing_key = 'config.users.{}.forwards.{}.updated'.format(resource_uuid, forward_name)
        self.required_acl = 'events.{}'.format(self.routing_key)

    def marshal(self):
        return {
            'uuid': self.uuid,
            'enabled': self.forward_enabled,
            'destination': self.forward_destination
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['uuid'],
                   msg['enabled'],
                   msg['destination'])
