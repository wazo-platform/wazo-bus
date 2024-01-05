# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from .types import DeviceDict, LineDict


class LineDeviceAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_device_associated'
    routing_key_fmt = 'config.lines.{line[id]}.devices.{device[id]}.updated'

    def __init__(self, line: LineDict, device: DeviceDict, tenant_uuid: str):
        content = {'line': line, 'device': device}
        super().__init__(content, tenant_uuid)


class LineDeviceDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_device_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.devices.{device[id]}.deleted'

    def __init__(self, line: LineDict, device: DeviceDict, tenant_uuid: str):
        content = {'line': line, 'device': device}
        super().__init__(content, tenant_uuid)
