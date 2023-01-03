# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class CallPermissionCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_permission_created'
    routing_key_fmt = 'config.callpermission.created'

    def __init__(self, call_permission_id, tenant_uuid):
        content = {'id': call_permission_id}
        super().__init__(content, tenant_uuid)


class CallPermissionDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'call_permission_deleted'
    routing_key_fmt = 'config.callpermission.deleted'

    def __init__(self, call_permission_id, tenant_uuid):
        content = {'id': call_permission_id}
        super().__init__(content, tenant_uuid)


class CallPermissionEditedEvent(TenantEvent):
    service = 'confd'
    name = 'call_permission_edited'
    routing_key_fmt = 'config.callpermission.edited'

    def __init__(self, call_permission_id, tenant_uuid):
        content = {'id': call_permission_id}
        super().__init__(content, tenant_uuid)
