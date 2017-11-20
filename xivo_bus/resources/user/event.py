# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class ResourceWithUUIDConfigEvent(ResourceConfigEvent):

    def __init__(self, resource_id, resource_uuid):
        super(ResourceWithUUIDConfigEvent, self).__init__(resource_id)
        self.uuid = resource_uuid

    def marshal(self):
        dict_ = super(ResourceWithUUIDConfigEvent, self).marshal()
        dict_['uuid'] = self.uuid
        return dict_

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['uuid'])

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


class EditUserEvent(ResourceWithUUIDConfigEvent):

    name = 'user_edited'
    routing_key = 'config.user.edited'


class CreateUserEvent(ResourceWithUUIDConfigEvent):

    name = 'user_created'
    routing_key = 'config.user.created'


class DeleteUserEvent(ResourceWithUUIDConfigEvent):

    name = 'user_deleted'
    routing_key = 'config.user.deleted'


class EditUserFallbackEvent(ResourceWithUUIDConfigEvent):
    name = 'user_fallback_edited'
    routing_key = 'config.users.fallbacks.edited'


class _BaseConfigUserEvent(object):
    def __init__(self, user_uuid):
        self.user_uuid = user_uuid

    def __eq__(self, other):
        return self.user_uuid == other.user_uuid

    def __ne__(self, other):
        return not self == other


class EditUserServiceEvent(_BaseConfigUserEvent):
    def __init__(self, user_uuid, service_name, service_enabled):
        super(EditUserServiceEvent, self).__init__(user_uuid)
        self.service_enabled = service_enabled
        self.name = 'users_services_{}_updated'.format(service_name)
        self.routing_key = 'config.users.{}.services.{}.updated'.format(user_uuid, service_name)
        self.required_acl = 'events.{}'.format(self.routing_key)

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'enabled': self.service_enabled
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['user_uuid'],
                   msg['enabled'])


class EditUserForwardEvent(_BaseConfigUserEvent):
    def __init__(self, user_uuid, forward_name, forward_enabled, forward_destination):
        super(EditUserForwardEvent, self).__init__(user_uuid)
        self.forward_enabled = forward_enabled
        self.forward_destination = forward_destination
        self.name = 'users_forwards_{}_updated'.format(forward_name)
        self.routing_key = 'config.users.{}.forwards.{}.updated'.format(user_uuid, forward_name)
        self.required_acl = 'events.{}'.format(self.routing_key)

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'enabled': self.forward_enabled,
            'destination': self.forward_destination
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['user_uuid'],
                   msg['enabled'],
                   msg['destination'])
