# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class GroupCallPermissionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_call_permission_associated'
    routing_key_fmt = 'config.groups.{group_uuid}.callpermissions.updated'

    def __init__(
        self, group_id: int, group_uuid: str, call_permission_id: int, tenant_uuid: str
    ):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'call_permission_id': call_permission_id,
        }
        super().__init__(content, tenant_uuid)


class GroupCallPermissionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_call_permission_dissociated'
    routing_key_fmt = 'config.groups.{group_uuid}.callpermissions.deleted'

    def __init__(
        self, group_id: int, group_uuid: str, call_permission_id: int, tenant_uuid: str
    ):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'call_permission_id': call_permission_id,
        }
        super().__init__(content, tenant_uuid)
