# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class GroupCallPermissionAssociatedEvent(TenantEvent):
    name = 'group_call_permission_associated'
    routing_key_fmt = 'config.groups.{group_uuid}.callpermissions.updated'

    def __init__(self, group_id, group_uuid, call_permission_id, tenant_uuid):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'call_permission_id': call_permission_id,
        }
        super(GroupCallPermissionAssociatedEvent, self).__init__(content, tenant_uuid)


class GroupCallPermissionDissociatedEvent(TenantEvent):
    name = 'group_call_permission_dissociated'
    routing_key_fmt = 'config.groups.{group_uuid}.callpermissions.deleted'

    def __init__(self, group_id, group_uuid, call_permission_id, tenant_uuid):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'call_permission_id': call_permission_id,
        }
        super(GroupCallPermissionDissociatedEvent, self).__init__(content, tenant_uuid)
