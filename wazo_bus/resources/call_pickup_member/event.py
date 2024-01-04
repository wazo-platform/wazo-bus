# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class CallPickupInterceptorUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_interceptor_users_associated'
    routing_key_fmt = 'config.callpickups.interceptors.users.updated'

    def __init__(
        self,
        call_pickup_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_pickup_id': call_pickup_id,
            'user_uuids': users,
        }
        super().__init__(content, tenant_uuid)


class CallPickupTargetUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_target_users_associated'
    routing_key_fmt = 'config.callpickups.targets.users.updated'

    def __init__(
        self,
        call_pickup_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_pickup_id': call_pickup_id,
            'user_uuids': users,
        }
        super().__init__(content, tenant_uuid)


class CallPickupInterceptorGroupsAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_interceptor_groups_associated'
    routing_key_fmt = 'config.callpickups.interceptors.groups.updated'

    def __init__(
        self,
        call_pickup_id: int,
        group_ids: list[int],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_pickup_id': call_pickup_id,
            'group_ids': group_ids,
        }
        super().__init__(content, tenant_uuid)


class CallPickupTargetGroupsAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_target_groups_associated'
    routing_key_fmt = 'config.callpickups.targets.groups.updated'

    def __init__(
        self,
        call_pickup_id: int,
        group_ids: list[int],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_pickup_id': call_pickup_id,
            'group_ids': group_ids,
        }
        super().__init__(content, tenant_uuid)
