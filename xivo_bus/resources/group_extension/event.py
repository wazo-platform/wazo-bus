# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class GroupExtensionAssociatedEvent(TenantEvent):
    name = 'group_extension_associated'
    routing_key_fmt = 'config.groups.extensions.updated'

    def __init__(self, group_id, group_uuid, extension_id, tenant_uuid):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'extension_id': extension_id,
        }
        super(GroupExtensionAssociatedEvent, self).__init__(content, tenant_uuid)


class GroupExtensionDissociatedEvent(TenantEvent):
    name = 'group_extension_dissociated'
    routing_key_fmt = 'config.groups.extensions.deleted'

    def __init__(self, group_id, group_uuid, extension_id, tenant_uuid):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'extension_id': extension_id,
        }
        super(GroupExtensionDissociatedEvent, self).__init__(content, tenant_uuid)
