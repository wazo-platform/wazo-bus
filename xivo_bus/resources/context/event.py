# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class ContextCreatedEvent(TenantEvent):
    name = 'context_created'
    routing_key_fmt = 'config.contexts.created'

    def __init__(self, context_data, tenant_uuid):
        super(ContextCreatedEvent, self).__init__(context_data, tenant_uuid)


class ContextDeletedEvent(TenantEvent):
    name = 'context_deleted'
    routing_key_fmt = 'config.contexts.deleted'

    def __init__(self, context_data, tenant_uuid):
        super(ContextDeletedEvent, self).__init__(context_data, tenant_uuid)


class ContextEditedEvent(TenantEvent):
    name = 'context_edited'
    routing_key_fmt = 'config.contexts.edited'

    def __init__(self, context_data, tenant_uuid):
        super(ContextEditedEvent, self).__init__(context_data, tenant_uuid)
