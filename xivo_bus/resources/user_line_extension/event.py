# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import UserEvent
from ..common.types import UUIDStr


class _BaseUserLineExtensionEvent(UserEvent):
    def __init__(
        self,
        user_line_extension_id: int,
        user_id: int,
        line_id: int,
        extension_id: int,
        main_user: bool,
        main_line: bool,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'id': int(user_line_extension_id),
            'user_id': int(user_id),
            'line_id': int(line_id),
            'extension_id': int(extension_id),
            'main_user': bool(main_user),
            'main_line': bool(main_line),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserLineExtensionCreatedEvent(_BaseUserLineExtensionEvent):
    service = 'confd'
    name = 'user_line_extension_created'
    routing_key_fmt = 'config.users.lines.extensions.created'


class UserLineExtensionDeletedEvent(_BaseUserLineExtensionEvent):
    service = 'confd'
    name = 'user_line_extension_deleted'
    routing_key_fmt = 'config.users.lines.extensions.deleted'


class UserLineExtensionEditedEvent(_BaseUserLineExtensionEvent):
    service = 'confd'
    name = 'user_line_extension_edited'
    routing_key_fmt = 'config.users.lines.extensions.edited'
