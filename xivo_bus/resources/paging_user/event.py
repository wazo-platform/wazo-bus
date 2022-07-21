# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class PagingCallerUsersAssociatedEvent(TenantEvent):
    name = 'paging_caller_users_associated'
    routing_key_fmt = 'config.pagings.callers.users.updated'

    def __init__(self, paging_id, users, tenant_uuid):
        content = {
            'paging_id': paging_id,
            'user_uuids': users,
        }
        super(PagingCallerUsersAssociatedEvent, self).__init__(content, tenant_uuid)


class PagingMemberUsersAssociatedEvent(TenantEvent):
    name = 'paging_member_users_associated'
    routing_key_fmt = 'config.pagings.members.users.updated'

    def __init__(self, paging_id, users, tenant_uuid):
        content = {
            'paging_id': paging_id,
            'user_uuids': users,
        }
        super(PagingMemberUsersAssociatedEvent, self).__init__(content, tenant_uuid)
