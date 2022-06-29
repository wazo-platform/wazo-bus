# -*- coding: utf-8 -*-
# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from .abstract import AbstractEvent


class ServiceEvent(AbstractEvent):
    pass


class TenantEvent(AbstractEvent):
    def __init__(self, content, tenant_uuid):
        super(TenantEvent, self).__init__(content=content)
        if tenant_uuid is None:
            raise ValueError('tenant_uuid must have a value')
        self.tenant_uuid = str(tenant_uuid)


class UserEvent(TenantEvent):
    def __init__(self, content, tenant_uuid, user_uuid):
        super(UserEvent, self).__init__(content, tenant_uuid)
        if user_uuid is None:
            raise ValueError('user_uuid must have a value')
        self.user_uuid = str(user_uuid)

    @property
    def headers(self):
        headers = super(UserEvent, self).headers
        uuid = headers.pop('user_uuid')
        headers['user_uuid:{}'.format(uuid)] = True
        return headers


# Deprecated and should not be used for new events
class BaseEvent(object):
    def __init__(self):
        self.routing_key = self.routing_key_fmt.format(**self._body)
        self.required_acl = 'events.{}'.format(self.routing_key)

    def marshal(self):
        return self._body

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._body == other._body

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self._body)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def unmarshal(cls, body):
        return cls(**body)


# Deprecated and should not be used for new events
class ResourceConfigEvent(object):
    def __init__(self, resource_id):
        self.id = int(resource_id)

    def marshal(self):
        return {'id': self.id}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'])

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id


# Deprecated and should not be used for new events
class ArbitraryEvent(object):
    def __init__(self, name, body, required_acl=None):
        self.name = name
        self._body = dict(body)
        if required_acl:
            self.required_acl = required_acl

    def marshal(self):
        return self._body

    def __eq__(self, other):
        return (
            self.name == other.name
            and self._body == other._body
            and self.required_acl == other.required_acl
        )

    def __ne__(self, other):
        return self != other
