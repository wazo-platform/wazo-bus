# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class OutcallScheduleAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_schedule_associated'
    routing_key_fmt = 'config.outcalls.schedules.updated'

    def __init__(self, outcall_id, schedule_id, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'schedule_id': schedule_id,
        }
        super(OutcallScheduleAssociatedEvent, self).__init__(content, tenant_uuid)


class OutcallScheduleDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_schedule_dissociated'
    routing_key_fmt = 'config.outcalls.schedules.deleted'

    def __init__(self, outcall_id, schedule_id, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'schedule_id': schedule_id,
        }
        super(OutcallScheduleDissociatedEvent, self).__init__(content, tenant_uuid)
