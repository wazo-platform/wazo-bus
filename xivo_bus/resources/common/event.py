# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .abstract import AbstractEvent


class ServiceEvent(AbstractEvent):
    '''
    ### Service-level event base class

    These events are intended for internal use by services and will never
    make it through the websocket.
    '''

    pass


class TenantEvent(AbstractEvent):
    '''
    ### Tenant-level event base class

    These events are intended for *all* users of the specified tenant.  They will be
    dispatched to all it's connected users by setting `user_uuid:*` in the headers.

    #### Required property:
        - tenant_uuid
    '''

    def __init__(self, content, tenant_uuid):
        super().__init__(content=content)
        if tenant_uuid is None:
            raise ValueError('tenant_uuid must have a value')
        self.tenant_uuid = str(tenant_uuid)
        setattr(self, 'user_uuid:*', True)


class UserEvent(TenantEvent):
    '''
    ### User-level event base class

    These events are intended for a single user from a specific tenant.  They will be
    dispatched through the websocket to the user by setting `user_uuid:{uuid}`
    in the headers.

    #### Required properties:
        - tenant_uuid
        - user_uuid
    '''

    def __init__(self, content, tenant_uuid, user_uuid):
        super().__init__(content, tenant_uuid)
        delattr(self, 'user_uuid:*')
        self.user_uuid = str(user_uuid) if user_uuid else None

    @property
    def headers(self):
        headers = super().headers
        uuid = headers.pop('user_uuid')
        if uuid:
            headers['user_uuid:{}'.format(uuid)] = True
        return headers


class MultiUserEvent(TenantEvent):
    '''
    ### User-level event base class (targetting multiple users)

    These events are intended for multiple users from a specific tenant.
    They will be dispatched through the websocket by setting `user_uuid:{uuid} = True`
    in the headers for all intended users.

    #### Required properties:
        - tenant_uuid
        - list of user_uuids
    '''

    __slots__ = ('user_uuids',)

    def __init__(self, content, tenant_uuid, user_uuids):
        super().__init__(content, tenant_uuid)
        delattr(self, 'user_uuid:*')
        if not isinstance(user_uuids, list):
            raise ValueError('user_uuids must be a list of uuids')
        self.user_uuids = [str(user_uuid) for user_uuid in user_uuids]

    @property
    def headers(self):
        headers = super().headers
        for user_uuid in self.user_uuids:
            headers['user_uuid:{}'.format(user_uuid)] = True
        return headers


# Deprecated and should not be used for new events
class BaseEvent:
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
class ResourceConfigEvent:
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
class ArbitraryEvent:
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
