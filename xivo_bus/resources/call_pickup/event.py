# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class CallPickupCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_created'
    routing_key_fmt = 'config.callpickup.created'

    def __init__(self, call_pickup_id, tenant_uuid):
        content = {'id': call_pickup_id}
        super(CallPickupCreatedEvent, self).__init__(content, tenant_uuid)


class CallPickupDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_deleted'
    routing_key_fmt = 'config.callpickup.deleted'

    def __init__(self, call_pickup_id, tenant_uuid):
        content = {'id': call_pickup_id}
        super(CallPickupDeletedEvent, self).__init__(content, tenant_uuid)


class CallPickupEditedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_edited'
    routing_key_fmt = 'config.callpickup.edited'

    def __init__(self, call_pickup_id, tenant_uuid):
        content = {'id': call_pickup_id}
        super(CallPickupEditedEvent, self).__init__(content, tenant_uuid)
