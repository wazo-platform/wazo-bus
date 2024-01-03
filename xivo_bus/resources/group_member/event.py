# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format
from .types import GroupExtensionDict


class GroupMemberUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_member_users_associated'
    routing_key_fmt = 'config.groups.members.users.updated'

    def __init__(
        self,
        group_id: int,
        group_uuid: Annotated[str, Format('uuid')],
        users: list[str],
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'user_uuids': users,
        }
        super().__init__(content, tenant_uuid)


class GroupMemberExtensionsAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_member_extensions_associated'
    routing_key_fmt = 'config.groups.members.extensions.updated'

    def __init__(
        self,
        group_id: int,
        group_uuid: Annotated[str, Format('uuid')],
        extensions: list[GroupExtensionDict],
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'extensions': extensions,
        }
        super().__init__(content, tenant_uuid)
