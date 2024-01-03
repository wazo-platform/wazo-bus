# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from xivo_bus.resources.common.event import TenantEvent


class DeviceCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'device_created'
    routing_key_fmt = 'config.device.created'

    def __init__(self, device_id: str, tenant_uuid: Annotated[str, {'format': 'uuid'}]):
        content = {'id': device_id}
        super().__init__(content, tenant_uuid)


class DeviceDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'device_deleted'
    routing_key_fmt = 'config.device.deleted'

    def __init__(self, device_id: str, tenant_uuid: Annotated[str, {'format': 'uuid'}]):
        content = {'id': device_id}
        super().__init__(content, tenant_uuid)


class DeviceEditedEvent(TenantEvent):
    service = 'confd'
    name = 'device_edited'
    routing_key_fmt = 'config.device.edited'

    def __init__(self, device_id: str, tenant_uuid: Annotated[str, {'format': 'uuid'}]):
        content = {'id': device_id}
        super().__init__(content, tenant_uuid)
