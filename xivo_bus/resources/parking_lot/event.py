# -*- coding: utf-8 -*-
# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditParkingLotEvent(ResourceConfigEvent):
    name = 'parking_lot_edited'
    routing_key = 'config.parkinglots.edited'


class CreateParkingLotEvent(ResourceConfigEvent):
    name = 'parking_lot_created'
    routing_key = 'config.parkinglots.created'


class DeleteParkingLotEvent(ResourceConfigEvent):
    name = 'parking_lot_deleted'
    routing_key = 'config.parkinglots.deleted'
