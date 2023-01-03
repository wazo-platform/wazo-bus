# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class GroupMemberUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_member_users_associated'
    routing_key_fmt = 'config.groups.members.users.updated'

    def __init__(self, group_id, group_uuid, users, tenant_uuid):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'user_uuids': users,
        }
        super(GroupMemberUsersAssociatedEvent, self).__init__(content, tenant_uuid)


class GroupMemberExtensionsAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_member_extensions_associated'
    routing_key_fmt = 'config.groups.members.extensions.updated'

    def __init__(self, group_id, group_uuid, extensions, tenant_uuid):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'extensions': extensions,
        }
        super(GroupMemberExtensionsAssociatedEvent, self).__init__(content, tenant_uuid)
