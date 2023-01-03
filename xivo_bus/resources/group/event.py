# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class GroupCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_created'
    routing_key_fmt = 'config.groups.created'

    def __init__(self, group, tenant_uuid):
        super(GroupCreatedEvent, self).__init__(group, tenant_uuid)


class GroupDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'group_deleted'
    routing_key_fmt = 'config.groups.deleted'

    def __init__(self, group, tenant_uuid):
        super(GroupDeletedEvent, self).__init__(group, tenant_uuid)


class GroupEditedEvent(TenantEvent):
    service = 'confd'
    name = 'group_edited'
    routing_key_fmt = 'config.groups.edited'

    def __init__(self, group, tenant_uuid):
        super(GroupEditedEvent, self).__init__(group, tenant_uuid)


class GroupFallbackEditedEvent(TenantEvent):
    service = 'confd'
    name = 'group_fallback_edited'
    routing_key_fmt = 'config.groups.fallbacks.edited'

    def __init__(self, group_id, group_uuid, tenant_uuid):
        content = {
            'id': group_id,
            'uuid': str(group_uuid),
        }
        super(GroupFallbackEditedEvent, self).__init__(content, tenant_uuid)
