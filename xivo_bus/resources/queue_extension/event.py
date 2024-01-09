# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class QueueExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_extension_associated'
    routing_key_fmt = 'config.queues.extensions.updated'

    def __init__(
        self,
        queue_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'queue_id': queue_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)


class QueueExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_extension_dissociated'
    routing_key_fmt = 'config.queues.extensions.deleted'

    def __init__(
        self,
        queue_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'queue_id': queue_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)
