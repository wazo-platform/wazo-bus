# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class ParkingLotCreatedEvent(TenantEvent):
    name = 'parking_lot_created'
    routing_key_fmt = 'config.parkinglots.created'

    def __init__(self, parking_id, tenant_uuid):
        content = {'id': int(parking_id)}
        super(ParkingLotCreatedEvent, self).__init__(content, tenant_uuid)


class ParkingLotDeletedEvent(TenantEvent):
    name = 'parking_lot_deleted'
    routing_key_fmt = 'config.parkinglots.deleted'

    def __init__(self, parking_id, tenant_uuid):
        content = {'id': int(parking_id)}
        super(ParkingLotDeletedEvent, self).__init__(content, tenant_uuid)


class ParkingLotEditedEvent(TenantEvent):
    name = 'parking_lot_edited'
    routing_key_fmt = 'config.parkinglots.edited'

    def __init__(self, parking_id, tenant_uuid):
        content = {'id': int(parking_id)}
        super(ParkingLotEditedEvent, self).__init__(content, tenant_uuid)
