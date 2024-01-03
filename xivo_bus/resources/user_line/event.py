# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import UserEvent
from ..common.types import Format
from .types import LineDict, UserDict


class UserLineAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_line_associated'
    routing_key_fmt = 'config.users.{user_uuid}.lines.{line[id]}.updated'

    def __init__(
        self,
        user: UserDict,
        line: LineDict,
        main_user: bool,
        main_line: bool,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'line': line,
            'main_line': main_line,
            'main_user': main_user,
            'user': user,
        }
        super().__init__(content, tenant_uuid, user['uuid'])


class UserLineDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_line_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.lines.{line[id]}.deleted'

    def __init__(
        self,
        user: UserDict,
        line: LineDict,
        main_user: bool,
        main_line: bool,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'line': line,
            'main_line': main_line,
            'main_user': main_user,
            'user': user,
        }
        super().__init__(content, tenant_uuid, user['uuid'])
