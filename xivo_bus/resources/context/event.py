# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class ContextCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'context_created'
    routing_key_fmt = 'config.contexts.created'

    def __init__(self, context_data, tenant_uuid):
        super().__init__(context_data, tenant_uuid)


class ContextDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'context_deleted'
    routing_key_fmt = 'config.contexts.deleted'

    def __init__(self, context_data, tenant_uuid):
        super().__init__(context_data, tenant_uuid)


class ContextEditedEvent(TenantEvent):
    service = 'confd'
    name = 'context_edited'
    routing_key_fmt = 'config.contexts.edited'

    def __init__(self, context_data, tenant_uuid):
        super().__init__(context_data, tenant_uuid)
