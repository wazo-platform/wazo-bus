# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class GroupCallPermissionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_call_permission_associated'
    routing_key_fmt = 'config.groups.{group_uuid}.callpermissions.updated'

    def __init__(
        self,
        group_id: int,
        group_uuid: Annotated[str, Format('uuid')],
        call_permission_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
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
        self,
        group_id: int,
        group_uuid: Annotated[str, Format('uuid')],
        call_permission_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'call_permission_id': call_permission_id,
        }
        super().__init__(content, tenant_uuid)
