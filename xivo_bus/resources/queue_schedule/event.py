# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class QueueScheduleAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_schedule_associated'
    routing_key_fmt = 'config.queues.schedules.updated'

    def __init__(
        self,
        queue_id: int,
        schedule_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'queue_id': queue_id,
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid)


class QueueScheduleDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_schedule_dissociated'
    routing_key_fmt = 'config.queues.schedules.deleted'

    def __init__(
        self,
        queue_id: int,
        schedule_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'queue_id': queue_id,
            'schedule_id': schedule_id,
        }
        super().__init__(content, tenant_uuid)
