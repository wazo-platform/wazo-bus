# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class ScheduleCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'schedule_created'
    routing_key_fmt = 'config.schedules.created'

    def __init__(self, schedule_id, tenant_uuid):
        content = {'id': int(schedule_id)}
        super(ScheduleCreatedEvent, self).__init__(content, tenant_uuid)


class ScheduleDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'schedule_deleted'
    routing_key_fmt = 'config.schedules.deleted'

    def __init__(self, schedule_id, tenant_uuid):
        content = {'id': int(schedule_id)}
        super(ScheduleDeletedEvent, self).__init__(content, tenant_uuid)


class ScheduleEditedEvent(TenantEvent):
    service = 'confd'
    name = 'schedule_edited'
    routing_key_fmt = 'config.schedules.edited'

    def __init__(self, schedule_id, tenant_uuid):
        content = {'id': int(schedule_id)}
        super(ScheduleEditedEvent, self).__init__(content, tenant_uuid)
