# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class GroupScheduleAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_schedule_associated'
    routing_key_fmt = 'config.groups.schedules.updated'

    def __init__(self, group_id, group_uuid, schedule_id, tenant_uuid):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'schedule_id': schedule_id,
        }
        super(GroupScheduleAssociatedEvent, self).__init__(content, tenant_uuid)


class GroupScheduleDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_schedule_dissociated'
    routing_key_fmt = 'config.groups.schedules.deleted'

    def __init__(self, group_id, group_uuid, schedule_id, tenant_uuid):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'schedule_id': schedule_id,
        }
        super(GroupScheduleDissociatedEvent, self).__init__(content, tenant_uuid)
