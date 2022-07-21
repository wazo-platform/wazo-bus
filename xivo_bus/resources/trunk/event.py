# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, BaseEvent


class TrunkCreatedEvent(TenantEvent):
    name = 'trunk_created'
    routing_key_fmt = 'config.trunk.created'

    def __init__(self, trunk_id, tenant_uuid):
        content = {'id': int(trunk_id)}
        super(TrunkCreatedEvent, self).__init__(content, tenant_uuid)


class TrunkDeletedEvent(TenantEvent):
    name = 'trunk_deleted'
    routing_key_fmt = 'config.trunk.deleted'

    def __init__(self, trunk_id, tenant_uuid):
        content = {'id': int(trunk_id)}
        super(TrunkDeletedEvent, self).__init__(content, tenant_uuid)


class TrunkEditedEvent(TenantEvent):
    name = 'trunk_edited'
    routing_key_fmt = 'config.trunk.edited'

    def __init__(self, trunk_id, tenant_uuid):
        content = {'id': int(trunk_id)}
        super(TrunkEditedEvent, self).__init__(content, tenant_uuid)


class TrunkStatusUpdatedEvent(BaseEvent):

    name = 'trunk_status_updated'
    routing_key_fmt = 'trunks.{id}.status.updated'

    def __init__(self, status):
        self._body = status
        super(TrunkStatusUpdatedEvent, self).__init__()
