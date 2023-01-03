# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class QueueScheduleAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_schedule_associated'
    routing_key_fmt = 'config.queues.schedules.updated'

    def __init__(self, queue_id, schedule_id, tenant_uuid):
        content = {
            'queue_id': queue_id,
            'schedule_id': schedule_id,
        }
        super(QueueScheduleAssociatedEvent, self).__init__(content, tenant_uuid)


class QueueScheduleDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_schedule_dissociated'
    routing_key_fmt = 'config.queues.schedules.deleted'

    def __init__(self, queue_id, schedule_id, tenant_uuid):
        content = {
            'queue_id': queue_id,
            'schedule_id': schedule_id,
        }
        super(QueueScheduleDissociatedEvent, self).__init__(content, tenant_uuid)
