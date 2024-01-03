# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent


class PagingCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'paging_created'
    routing_key_fmt = 'config.pagings.created'

    def __init__(self, paging_id: int, tenant_uuid: Annotated[str, {'format': 'uuid'}]):
        content = {'id': paging_id}
        super().__init__(content, tenant_uuid)


class PagingDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'paging_deleted'
    routing_key_fmt = 'config.pagings.deleted'

    def __init__(self, paging_id: int, tenant_uuid: Annotated[str, {'format': 'uuid'}]):
        content = {'id': paging_id}
        super().__init__(content, tenant_uuid)


class PagingEditedEvent(TenantEvent):
    service = 'confd'
    name = 'paging_edited'
    routing_key_fmt = 'config.pagings.edited'

    def __init__(self, paging_id: int, tenant_uuid: Annotated[str, {'format': 'uuid'}]):
        content = {'id': paging_id}
        super().__init__(content, tenant_uuid)
