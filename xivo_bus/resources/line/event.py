# -*- coding: utf-8 -*-
# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class LineCreatedEvent(TenantEvent):
    name = 'line_created'
    routing_key_fmt = 'config.line.created'

    def __init__(self, line, tenant_uuid):
        super(LineCreatedEvent, self).__init__(line, tenant_uuid)


class LineDeletedEvent(TenantEvent):
    name = 'line_deleted'
    routing_key_fmt = 'config.line.deleted'

    def __init__(self, line, tenant_uuid):
        super(LineDeletedEvent, self).__init__(line, tenant_uuid)


class LineEditedEvent(TenantEvent):
    name = 'line_edited'
    routing_key_fmt = 'config.line.edited'

    def __init__(self, line, tenant_uuid):
        super(LineEditedEvent, self).__init__(line, tenant_uuid)


class LineStatusUpdatedEvent(TenantEvent):
    name = 'line_status_updated'
    routing_key_fmt = 'lines.{id}.status.updated'

    def __init__(self, status, tenant_uuid):
        super(LineStatusUpdatedEvent, self).__init__(status, tenant_uuid)
