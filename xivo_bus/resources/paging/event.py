# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class PagingCreatedEvent(TenantEvent):
    name = 'paging_created'
    routing_key_fmt = 'config.pagings.created'

    def __init__(self, paging_id, tenant_uuid):
        content = {'id': paging_id}
        super(PagingCreatedEvent, self).__init__(content, tenant_uuid)


class PagingDeletedEvent(TenantEvent):
    name = 'paging_deleted'
    routing_key_fmt = 'config.pagings.deleted'

    def __init__(self, paging_id, tenant_uuid):
        content = {'id': paging_id}
        super(PagingDeletedEvent, self).__init__(content, tenant_uuid)


class PagingEditedEvent(TenantEvent):
    name = 'paging_edited'
    routing_key_fmt = 'config.pagings.edited'

    def __init__(self, paging_id, tenant_uuid):
        content = {'id': paging_id}
        super(PagingEditedEvent, self).__init__(content, tenant_uuid)
