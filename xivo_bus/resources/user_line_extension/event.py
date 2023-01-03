# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import UserEvent


class _BaseUserLineExtensionEvent(UserEvent):
    def __init__(
        self,
        user_line_extension_id,
        user_id,
        line_id,
        extension_id,
        main_user,
        main_line,
        tenant_uuid,
        user_uuid,
    ):
        content = {
            'id': int(user_line_extension_id),
            'user_id': int(user_id),
            'line_id': int(line_id),
            'extension_id': int(extension_id),
            'main_user': bool(main_user),
            'main_line': bool(main_line),
        }
        super(_BaseUserLineExtensionEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


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
