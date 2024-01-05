# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent


class TrunkCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_created'
    routing_key_fmt = 'config.trunk.created'

    def __init__(self, trunk_id: int, tenant_uuid: str):
        content = {'id': int(trunk_id)}
        super().__init__(content, tenant_uuid)


class TrunkDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_deleted'
    routing_key_fmt = 'config.trunk.deleted'

    def __init__(self, trunk_id: int, tenant_uuid: str):
        content = {'id': int(trunk_id)}
        super().__init__(content, tenant_uuid)


class TrunkEditedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_edited'
    routing_key_fmt = 'config.trunk.edited'

    def __init__(self, trunk_id: int, tenant_uuid: str):
        content = {'id': int(trunk_id)}
        super().__init__(content, tenant_uuid)


class TrunkStatusUpdatedEvent(TenantEvent):
    service = 'calld'
    name = 'trunk_status_updated'
    routing_key_fmt = 'trunks.{id}.status.updated'

    def __init__(
        self,
        trunk_id: int,
        technology: str,
        endpoint_name: str,
        endpoint_registered: bool,
        endpoint_current_call_count: int,
        tenant_uuid: str,
    ):
        content = {
            'id': trunk_id,
            'technology': technology,
            'name': endpoint_name,
            'registered': endpoint_registered,
            'current_call_count': endpoint_current_call_count,
        }
        super().__init__(content, tenant_uuid)
