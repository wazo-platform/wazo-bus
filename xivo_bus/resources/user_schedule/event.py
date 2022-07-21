# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import UserEvent


class UserScheduleAssociatedEvent(UserEvent):
    name = 'user_schedule_associated'
    routing_key_fmt = 'config.users.schedules.updated'

    def __init__(self, schedule_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'schedule_id': schedule_id,
        }
        super(UserScheduleAssociatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class UserScheduleDissociatedEvent(UserEvent):
    name = 'user_schedule_dissociated'
    routing_key_fmt = 'config.users.schedules.deleted'

    def __init__(self, schedule_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'schedule_id': schedule_id,
        }
        super(UserScheduleDissociatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )
