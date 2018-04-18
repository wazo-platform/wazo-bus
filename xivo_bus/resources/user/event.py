# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class ResourceWithUUIDConfigEvent(ResourceConfigEvent):

    def __init__(self, id_, uuid, **kwargs):
        self.id = int(id_)
        self.uuid = str(uuid)
        self._body = {
            'id': self.id,
            'uuid': self.uuid,
            'subscription_type': kwargs.get('subscription_type'),
            'created_at': kwargs.get('created_at'),
        }

    def marshal(self):
        return self._body

    @classmethod
    def unmarshal(cls, body):
        body['id_'] = body.pop('id')
        return cls(**body)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._body == other._body

    def __ne__(self, other):
        return not self._body == other._body


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
