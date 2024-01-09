# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class ParkingLotExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'parking_lot_extension_associated'
    routing_key_fmt = 'config.parkinglots.extensions.updated'

    def __init__(
        self,
        parking_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'parking_lot_id': parking_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)


class ParkingLotExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'parking_lot_extension_dissociated'
    routing_key_fmt = 'config.parkinglots.extensions.deleted'

    def __init__(
        self,
        parking_id: int,
        extension_id: int,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'parking_lot_id': parking_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)
