# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class IncallCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_created'
    routing_key_fmt = 'config.incalls.created'

    def __init__(self, incall_id, tenant_uuid):
        content = {'id': incall_id}
        super(IncallCreatedEvent, self).__init__(content, tenant_uuid)


class IncallDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_deleted'
    routing_key_fmt = 'config.incalls.deleted'

    def __init__(self, incall_id, tenant_uuid):
        content = {'id': incall_id}
        super(IncallDeletedEvent, self).__init__(content, tenant_uuid)


class IncallEditedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_edited'
    routing_key_fmt = 'config.incalls.edited'

    def __init__(self, incall_id, tenant_uuid):
        content = {'id': incall_id}
        super(IncallEditedEvent, self).__init__(content, tenant_uuid)
