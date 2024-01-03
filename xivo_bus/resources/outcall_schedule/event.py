# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from xivo_bus.resources.common.event import TenantEvent


class OutcallScheduleAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_schedule_associated'
    routing_key_fmt = 'config.outcalls.schedules.updated'

    def __init__(
        self,
        outcall_id: int,
        schedule_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'outcall_id': outcall_id,
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid)


class OutcallScheduleDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_schedule_dissociated'
    routing_key_fmt = 'config.outcalls.schedules.deleted'

    def __init__(
        self,
        outcall_id: int,
        schedule_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'outcall_id': outcall_id,
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid)
