# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent


class ScheduleCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'schedule_created'
    routing_key_fmt = 'config.schedules.created'

    def __init__(
        self, schedule_id: int, tenant_uuid: Annotated[str, {'format': 'uuid'}]
    ):
        content = {'id': int(schedule_id)}
        super().__init__(content, tenant_uuid)


class ScheduleDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'schedule_deleted'
    routing_key_fmt = 'config.schedules.deleted'

    def __init__(
        self, schedule_id: int, tenant_uuid: Annotated[str, {'format': 'uuid'}]
    ):
        content = {'id': int(schedule_id)}
        super().__init__(content, tenant_uuid)


class ScheduleEditedEvent(TenantEvent):
    service = 'confd'
    name = 'schedule_edited'
    routing_key_fmt = 'config.schedules.edited'

    def __init__(
        self, schedule_id: int, tenant_uuid: Annotated[str, {'format': 'uuid'}]
    ):
        content = {'id': int(schedule_id)}
        super().__init__(content, tenant_uuid)
