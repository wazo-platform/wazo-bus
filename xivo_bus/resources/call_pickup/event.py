# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class CallPickupCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_created'
    routing_key_fmt = 'config.callpickup.created'

    def __init__(
        self, call_pickup_id: int, tenant_uuid: Annotated[str, Format('uuid')]
    ):
        content = {'id': call_pickup_id}
        super().__init__(content, tenant_uuid)


class CallPickupDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_deleted'
    routing_key_fmt = 'config.callpickup.deleted'

    def __init__(
        self, call_pickup_id: int, tenant_uuid: Annotated[str, Format('uuid')]
    ):
        content = {'id': call_pickup_id}
        super().__init__(content, tenant_uuid)


class CallPickupEditedEvent(TenantEvent):
    service = 'confd'
    name = 'call_pickup_edited'
    routing_key_fmt = 'config.callpickup.edited'

    def __init__(
        self, call_pickup_id: int, tenant_uuid: Annotated[str, Format('uuid')]
    ):
        content = {'id': call_pickup_id}
        super().__init__(content, tenant_uuid)
