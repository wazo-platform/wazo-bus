# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import UserEvent


class UserGroupsAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_groups_associated'
    routing_key_fmt = 'config.users.groups.updated'

    def __init__(self, group_ids: list[int], tenant_uuid: str, user_uuid: str):
        content = {
            'user_uuid': str(user_uuid),
            'group_ids': group_ids,
        }
        super().__init__(content, tenant_uuid, user_uuid)
