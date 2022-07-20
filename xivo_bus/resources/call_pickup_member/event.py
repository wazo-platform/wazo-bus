# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class CallPickupInterceptorUsersAssociatedEventt(TenantEvent):
    name = 'call_pickup_interceptor_users_associated'
    routing_key_fmt = 'config.callpickups.interceptors.users.updated'

    def __init__(self, call_pickup_id, users, tenant_uuid):
        content = {
            'call_pickup_id': call_pickup_id,
            'user_uuids': users,
        }
        super(CallPickupInterceptorUsersAssociatedEventt, self).__init__(
            content, tenant_uuid
        )


class CallPickupTargetUsersAssociatedEvent(TenantEvent):
    name = 'call_pickup_target_users_associated'
    routing_key_fmt = 'config.callpickups.targets.users.updated'

    def __init__(self, call_pickup_id, users, tenant_uuid):
        content = {
            'call_pickup_id': call_pickup_id,
            'user_uuids': users,
        }
        super(CallPickupTargetUsersAssociatedEvent, self).__init__(content, tenant_uuid)


class CallPickupInterceptorGroupsAssociatedEvent(TenantEvent):
    name = 'call_pickup_interceptor_groups_associated'
    routing_key_fmt = 'config.callpickups.interceptors.users.updated'

    def __init__(self, call_pickup_id, group_ids, tenant_uuid):
        content = {
            'call_pickup_id': call_pickup_id,
            'group_ids': group_ids,
        }
        super(CallPickupInterceptorGroupsAssociatedEvent, self).__init__(content, tenant_uuid)


class CallPickupTargetGroupsAssociatedEvent(TenantEvent):
    name = 'call_pickup_target_groups_associated'
    routing_key_fmt = 'config.callpickups.targets.groups.updated'

    def __init__(self, call_pickup_id, group_ids, tenant_uuid):
        content = {
            'call_pickup_id': call_pickup_id,
            'group_ids': group_ids,
        }
        super(CallPickupTargetGroupsAssociatedEvent, self).__init__(content, tenant_uuid)
