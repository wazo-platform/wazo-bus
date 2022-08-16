# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import UserEvent


class UserGroupsAssociatedEvent(UserEvent):
    name = 'user_groups_associated'
    routing_key_fmt = 'config.users.groups.updated'

    def __init__(self, group_ids, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'group_ids': group_ids,
        }
        super(UserGroupsAssociatedEvent, self).__init__(content, tenant_uuid, user_uuid)
