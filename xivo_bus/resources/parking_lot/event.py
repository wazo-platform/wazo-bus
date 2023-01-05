# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class ParkingLotCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'parking_lot_created'
    routing_key_fmt = 'config.parkinglots.created'

    def __init__(self, parking_id, tenant_uuid):
        content = {'id': int(parking_id)}
        super().__init__(content, tenant_uuid)


class ParkingLotDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'parking_lot_deleted'
    routing_key_fmt = 'config.parkinglots.deleted'

    def __init__(self, parking_id, tenant_uuid):
        content = {'id': int(parking_id)}
        super().__init__(content, tenant_uuid)


class ParkingLotEditedEvent(TenantEvent):
    service = 'confd'
    name = 'parking_lot_edited'
    routing_key_fmt = 'config.parkinglots.edited'

    def __init__(self, parking_id, tenant_uuid):
        content = {'id': int(parking_id)}
        super().__init__(content, tenant_uuid)
