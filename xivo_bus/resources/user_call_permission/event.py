# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import UserEvent


class UserCallPermissionAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_call_permission_associated'
    routing_key_fmt = 'config.users.{user_uuid}.callpermissions.updated'

    def __init__(self, call_permission_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'call_permission_id': call_permission_id,
        }
        super(UserCallPermissionAssociatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class UserCallPermissionDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_call_permission_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.callpermissions.deleted'

    def __init__(self, call_permission_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'call_permission_id': call_permission_id,
        }
        super(UserCallPermissionDissociatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )
