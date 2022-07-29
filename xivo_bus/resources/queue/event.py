# -*- coding: utf-8 -*-
# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, ResourceConfigEvent


class QueueCreatedEvent(TenantEvent):
    name = 'queue_created'
    routing_key_fmt = 'config.queues.created'

    def __init__(self, queue_id, tenant_uuid):
        content = {'id': int(queue_id)}
        super(QueueCreatedEvent, self).__init__(content, tenant_uuid)


class QueueDeletedEvent(TenantEvent):
    name = 'queue_deleted'
    routing_key_fmt = 'config.queues.deleted'

    def __init__(self, queue_id, tenant_uuid):
        content = {'id': int(queue_id)}
        super(QueueDeletedEvent, self).__init__(content, tenant_uuid)


class QueueEditedEvent(TenantEvent):
    name = 'queue_edited'
    routing_key_fmt = 'config.queues.edited'

    def __init__(self, queue_id, tenant_uuid):
        content = {'id': int(queue_id)}
        super(QueueEditedEvent, self).__init__(content, tenant_uuid)


class QueueFallbackEditedEvent(TenantEvent):
    name = 'queue_fallback_edited'
    routing_key_fmt = 'config.queues.fallbacks.edited'

    def __init__(self, queue_id, tenant_uuid):
        content = {'id': int(queue_id)}
        super(QueueFallbackEditedEvent, self).__init__(content, tenant_uuid)


# FIXME: Remove after wazo-agentd migration
class EditQueueEvent(ResourceConfigEvent):
    name = 'queue_edited'
    routing_key = 'config.queue.edited'


# FIXME: Remove after wazo-agentd migration
class DeleteQueueEvent(ResourceConfigEvent):
    name = 'queue_deleted'
    routing_key = 'config.queue.deleted'