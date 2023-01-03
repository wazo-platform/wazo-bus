# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import UserEvent


class UserLineAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_line_associated'
    routing_key_fmt = 'config.users.{user_uuid}.lines.{line[id]}.updated'

    def __init__(self, user, line, main_user, main_line, tenant_uuid):
        content = {
            'line': line,
            'main_line': main_line,
            'main_user': main_user,
            'user': user,
        }
        super(UserLineAssociatedEvent, self).__init__(
            content, tenant_uuid, user['uuid']
        )


class UserLineDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_line_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.lines.{line[id]}.deleted'

    def __init__(self, user, line, main_user, main_line, tenant_uuid):
        content = {
            'line': line,
            'main_line': main_line,
            'main_user': main_user,
            'user': user,
        }
        super(UserLineDissociatedEvent, self).__init__(
            content, tenant_uuid, user['uuid']
        )
