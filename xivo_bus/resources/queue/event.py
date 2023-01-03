# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class QueueCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_created'
    routing_key_fmt = 'config.queues.created'

    def __init__(self, queue_id, tenant_uuid):
        content = {'id': int(queue_id)}
        super(QueueCreatedEvent, self).__init__(content, tenant_uuid)


class QueueDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_deleted'
    routing_key_fmt = 'config.queues.deleted'

    def __init__(self, queue_id, tenant_uuid):
        content = {'id': int(queue_id)}
        super(QueueDeletedEvent, self).__init__(content, tenant_uuid)


class QueueEditedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_edited'
    routing_key_fmt = 'config.queues.edited'

    def __init__(self, queue_id, tenant_uuid):
        content = {'id': int(queue_id)}
        super(QueueEditedEvent, self).__init__(content, tenant_uuid)


class QueueFallbackEditedEvent(TenantEvent):
    service = 'confd'
    name = 'queue_fallback_edited'
    routing_key_fmt = 'config.queues.fallbacks.edited'

    def __init__(self, queue_id, tenant_uuid):
        content = {'id': int(queue_id)}
        super(QueueFallbackEditedEvent, self).__init__(content, tenant_uuid)
