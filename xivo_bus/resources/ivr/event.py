# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from xivo_bus.resources.common.event import TenantEvent


class IVRCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'ivr_created'
    routing_key_fmt = 'config.ivr.created'

    def __init__(self, ivr_id: int, tenant_uuid: Annotated[str, {'format': 'uuid'}]):
        content = {'id': ivr_id}
        super().__init__(content, tenant_uuid)


class IVRDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'ivr_deleted'
    routing_key_fmt = 'config.ivr.deleted'

    def __init__(self, ivr_id: int, tenant_uuid: Annotated[str, {'format': 'uuid'}]):
        content = {'id': ivr_id}
        super().__init__(content, tenant_uuid)


class IVREditedEvent(TenantEvent):
    service = 'confd'
    name = 'ivr_edited'
    routing_key_fmt = 'config.ivr.edited'

    def __init__(self, ivr_id: int, tenant_uuid: Annotated[str, {'format': 'uuid'}]):
        content = {'id': ivr_id}
        super().__init__(content, tenant_uuid)
