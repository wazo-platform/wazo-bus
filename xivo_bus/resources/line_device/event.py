# -*- coding: utf-8 -*-
# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class LineDeviceAssociatedEvent(TenantEvent):
    name = 'line_device_associated'
    routing_key_fmt = 'config.lines.{line[id]}.devices.{device[id]}.updated'

    def __init__(self, line, device, tenant_uuid):
        content = {'line': line, 'device': device}
        super(LineDeviceAssociatedEvent, self).__init__(content, tenant_uuid)


class LineDeviceDissociatedEvent(TenantEvent):
    name = 'line_device_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.devices.{device[id]}.deleted'

    def __init__(self, line, device, tenant_uuid):
        content = {'line': line, 'device': device}
        super(LineDeviceDissociatedEvent, self).__init__(content, tenant_uuid)
