# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class CallPermissionCreatedEvent(TenantEvent):
    name = 'call_permission_created'
    routing_key_fmt = 'config.callpermission.created'

    def __init__(self, call_permission_id, tenant_uuid):
        content = {'id': call_permission_id}
        super(CallPermissionCreatedEvent, self).__init__(content, tenant_uuid)


class CallPermissionDeletedEvent(TenantEvent):
    name = 'call_permission_deleted'
    routing_key_fmt = 'config.callpermission.deleted'

    def __init__(self, call_permission_id, tenant_uuid):
        content = {'id': call_permission_id}
        super(CallPermissionDeletedEvent, self).__init__(content, tenant_uuid)


class CallPermissionEditedEvent(TenantEvent):
    name = 'call_permission_edited'
    routing_key_fmt = 'config.callpermission.edited'

    def __init__(self, call_permission_id, tenant_uuid):
        content = {'id': call_permission_id}
        super(CallPermissionEditedEvent, self).__init__(content, tenant_uuid)
