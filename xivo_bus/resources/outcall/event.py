# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class OutcallCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_created'
    routing_key_fmt = 'config.outcalls.created'

    def __init__(self, outcall_id: int, tenant_uuid: Annotated[str, Format('uuid')]):
        content = {'id': outcall_id}
        super().__init__(content, tenant_uuid)


class OutcallDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_deleted'
    routing_key_fmt = 'config.outcalls.deleted'

    def __init__(self, outcall_id: int, tenant_uuid: Annotated[str, Format('uuid')]):
        content = {'id': outcall_id}
        super().__init__(content, tenant_uuid)


class OutcallEditedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_edited'
    routing_key_fmt = 'config.outcalls.edited'

    def __init__(self, outcall_id: int, tenant_uuid: Annotated[str, Format('uuid')]):
        content = {'id': outcall_id}
        super().__init__(content, tenant_uuid)
