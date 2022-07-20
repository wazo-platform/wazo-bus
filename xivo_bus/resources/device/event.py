# -*- coding: utf-8 -*-
# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class DeviceCreatedEvent(TenantEvent):
    name = 'device_created'
    routing_key_fmt = 'config.device.created'

    def __init__(self, device_id, tenant_uuid):
        content = {'id': device_id}
        super(DeviceCreatedEvent, self).__init__(content, tenant_uuid)


class DeviceDeletedEvent(TenantEvent):
    name = 'device_deleted'
    routing_key_fmt = 'config.device.deleted'

    def __init__(self, device_id, tenant_uuid):
        content = {'id': device_id}
        super(DeviceCreatedEvent, self).__init__(content, tenant_uuid)


class DeviceEditedEvent(TenantEvent):
    name = 'device_edited'
    routing_key_fmt = 'config.device.edited'

    def __init__(self, device_id, tenant_uuid):
        content = {'id': device_id}
        super(DeviceCreatedEvent, self).__init__(content, tenant_uuid)
