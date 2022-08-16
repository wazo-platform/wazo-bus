# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class QueueExtensionAssociatedEvent(TenantEvent):
    name = 'queue_extension_associated'
    routing_key_fmt = 'config.queues.extensions.updated'

    def __init__(self, queue_id, extension_id, tenant_uuid):
        content = {
            'queue_id': queue_id,
            'extension_id': extension_id,
        }
        super(QueueExtensionAssociatedEvent, self).__init__(content, tenant_uuid)


class QueueExtensionDissociatedEvent(TenantEvent):
    name = 'queue_extension_dissociated'
    routing_key_fmt = 'config.queues.extensions.deleted'

    def __init__(self, queue_id, extension_id, tenant_uuid):
        content = {
            'queue_id': queue_id,
            'extension_id': extension_id,
        }
        super(QueueExtensionDissociatedEvent, self).__init__(content, tenant_uuid)
