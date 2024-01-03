# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent


class OutcallCallPermissionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_call_permission_associated'
    routing_key_fmt = 'config.outcalls.{outcall_id}.callpermissions.updated'

    def __init__(
        self,
        outcall_id: int,
        call_permission_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'outcall_id': outcall_id,
            'call_permission_id': call_permission_id,
        }
        super().__init__(content, tenant_uuid)


class OutcallCallPermissionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_call_permission_dissociated'
    routing_key_fmt = 'config.outcalls.{outcall_id}.callpermissions.deleted'

    def __init__(
        self,
        outcall_id: int,
        call_permission_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'outcall_id': outcall_id,
            'call_permission_id': call_permission_id,
        }
        super().__init__(content, tenant_uuid)
