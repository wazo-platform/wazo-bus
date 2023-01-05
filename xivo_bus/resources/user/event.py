# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent, UserEvent


class _BaseUserEvent(TenantEvent):
    def __init__(self, user_id, user_uuid, subscription_type, created_at, tenant_uuid):
        content = {
            'id': int(user_id),
            'uuid': str(user_uuid),
            'subscription_type': subscription_type,
            'created_at': str(created_at) if created_at is not None else None,
            'tenant_uuid': str(tenant_uuid),
        }
        super().__init__(content, tenant_uuid)


class UserCreatedEvent(_BaseUserEvent):
    service = 'confd'
    name = 'user_created'
    routing_key_fmt = 'config.user.created'


class UserDeletedEvent(_BaseUserEvent):
    service = 'confd'
    name = 'user_deleted'
    routing_key_fmt = 'config.user.deleted'


class UserEditedEvent(_BaseUserEvent):
    service = 'confd'
    name = 'user_edited'
    routing_key_fmt = 'config.user.edited'


class UserFallbackEditedEvent(UserEvent):
    service = 'confd'
    name = 'user_fallback_edited'
    routing_key_fmt = 'config.users.fallbacks.edited'

    def __init__(self, user_id, tenant_uuid, user_uuid):
        content = {
            'id': int(user_id),
            'uuid': str(user_uuid),
            'subscription_type': None,
            'created_at': None,
            'tenant_uuid': str(tenant_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserServiceEditedEvent(UserEvent):
    service = 'confd'
    name = 'users_services_{service_name}_updated'
    routing_key_fmt = 'config.users.{user_uuid}.services.{service_name}.updated'

    def __init__(self, user_id, service_name, service_enabled, tenant_uuid, user_uuid):
        self.name = type(self).name.format(service_name=service_name)
        content = {
            'user_id': int(user_id),
            'user_uuid': str(user_uuid),
            'tenant_uuid': str(tenant_uuid),
            'enabled': service_enabled,
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.service_name = service_name


class UserForwardEditedEvent(UserEvent):
    service = 'confd'
    name = 'users_forwards_{forward_name}_updated'
    routing_key_fmt = 'config.users.{user_uuid}.forwards.{forward_name}.updated'

    def __init__(
        self,
        user_id,
        forward_name,
        forward_enabled,
        forward_dest,
        tenant_uuid,
        user_uuid,
    ):
        self.name = type(self).name.format(forward_name=forward_name)
        content = {
            'user_id': int(user_id),
            'user_uuid': str(user_uuid),
            'tenant_uuid': str(tenant_uuid),
            'enabled': forward_enabled,
            'destination': forward_dest,
        }
        super().__init__(content, tenant_uuid, user_uuid)
        self.forward_name = forward_name
