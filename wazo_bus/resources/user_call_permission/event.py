# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import UserEvent
from ..common.types import UUIDStr


class UserCallPermissionAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_call_permission_associated'
    routing_key_fmt = 'config.users.{user_uuid}.callpermissions.updated'

    def __init__(
        self,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'call_permission_id': call_permission_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserCallPermissionDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_call_permission_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.callpermissions.deleted'

    def __init__(
        self,
        call_permission_id: int,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'user_uuid': str(user_uuid),
            'call_permission_id': call_permission_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
