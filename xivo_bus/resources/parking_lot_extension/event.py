# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class ParkingLotExtensionAssociatedEvent(TenantEvent):
    name = 'parking_lot_extension_associated'
    routing_key_fmt = 'config.parkinglots.extensions.updated'

    def __init__(self, parking_id, extension_id, tenant_uuid):
        content = {
            'parking_lot_id': parking_id,
            'extension_id': extension_id,
        }
        super(ParkingLotExtensionAssociatedEvent, self).__init__(content, tenant_uuid)


class ParkingLotExtensionDissociatedEvent(TenantEvent):
    name = 'parking_lot_extension_dissociated'
    routing_key_fmt = 'config.parkinglots.extensions.deleted'

    def __init__(self, parking_id, extension_id, tenant_uuid):
        content = {
            'parking_lot_id': parking_id,
            'extension_id': extension_id,
        }
        super(ParkingLotExtensionDissociatedEvent, self).__init__(content, tenant_uuid)
