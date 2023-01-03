# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class QueueExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_extension_associated'
    routing_key_fmt = 'config.queues.extensions.updated'

    def __init__(self, queue_id, extension_id, tenant_uuid):
        content = {
            'queue_id': queue_id,
            'extension_id': extension_id,
        }
        super(QueueExtensionAssociatedEvent, self).__init__(content, tenant_uuid)


class QueueExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_extension_dissociated'
    routing_key_fmt = 'config.queues.extensions.deleted'

    def __init__(self, queue_id, extension_id, tenant_uuid):
        content = {
            'queue_id': queue_id,
            'extension_id': extension_id,
        }
        super(QueueExtensionDissociatedEvent, self).__init__(content, tenant_uuid)
