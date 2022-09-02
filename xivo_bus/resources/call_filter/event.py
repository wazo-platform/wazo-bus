# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class CallFilterCreatedEvent(TenantEvent):
    name = 'call_filter_created'
    routing_key_fmt = 'config.callfilter.created'

    def __init__(self, call_filter_id, tenant_uuid):
        content = {'id': call_filter_id}
        super(CallFilterCreatedEvent, self).__init__(content, tenant_uuid)


class CallFilterDeletedEvent(TenantEvent):
    name = 'call_filter_deleted'
    routing_key_fmt = 'config.callfilter.deleted'

    def __init__(self, call_filter_id, tenant_uuid):
        content = {'id': call_filter_id}
        super(CallFilterDeletedEvent, self).__init__(content, tenant_uuid)


class CallFilterEditedEvent(TenantEvent):
    name = 'call_filter_edited'
    routing_key_fmt = 'config.callfilter.edited'

    def __init__(self, call_filter_id, tenant_uuid):
        content = {'id': call_filter_id}
        super(CallFilterEditedEvent, self).__init__(content, tenant_uuid)


class CallFilterFallbackEditedEvent(TenantEvent):
    name = 'call_filter_fallback_edited'
    routing_key_fmt = 'config.callfilters.fallbacks.edited'

    def __init__(self, call_filter_id, tenant_uuid):
        content = {'id': call_filter_id}
        super(CallFilterFallbackEditedEvent, self).__init__(content, tenant_uuid)
