# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class IncallScheduleAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_schedule_associated'
    routing_key_fmt = 'config.incalls.schedules.updated'

    def __init__(self, incall_id, schedule_id, tenant_uuid):
        content = {
            'incall_id': incall_id,
            'schedule_id': schedule_id,
        }
        super(IncallScheduleAssociatedEvent, self).__init__(content, tenant_uuid)


class IncallScheduleDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_schedule_dissociated'
    routing_key_fmt = 'config.incalls.schedules.deleted'

    def __init__(self, incall_id, schedule_id, tenant_uuid):
        content = {
            'incall_id': incall_id,
            'schedule_id': schedule_id,
        }
        super(IncallScheduleDissociatedEvent, self).__init__(content, tenant_uuid)
