# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class CallPermissionCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_permission_created'
    routing_key_fmt = 'config.callpermission.created'

    def __init__(
        self, call_permission_id: int, tenant_uuid: Annotated[str, Format('uuid')]
    ):
        content = {'id': call_permission_id}
        super().__init__(content, tenant_uuid)


class CallPermissionDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'call_permission_deleted'
    routing_key_fmt = 'config.callpermission.deleted'

    def __init__(
        self, call_permission_id: int, tenant_uuid: Annotated[str, Format('uuid')]
    ):
        content = {'id': call_permission_id}
        super().__init__(content, tenant_uuid)


class CallPermissionEditedEvent(TenantEvent):
    service = 'confd'
    name = 'call_permission_edited'
    routing_key_fmt = 'config.callpermission.edited'

    def __init__(
        self, call_permission_id: int, tenant_uuid: Annotated[str, Format('uuid')]
    ):
        content = {'id': call_permission_id}
        super().__init__(content, tenant_uuid)
