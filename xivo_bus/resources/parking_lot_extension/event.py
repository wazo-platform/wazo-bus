# -*- coding: utf-8 -*-

# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class ParkingLotExtensionConfigEvent(object):

    def __init__(self, parking_lot_id, extension_id):
        self.parking_lot_id = parking_lot_id
        self.extension_id = extension_id

    def marshal(self):
        return {
            'parking_lot_id': self.parking_lot_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['parking_lot_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.parking_lot_id == other.parking_lot_id and
                self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not self == other


class ParkingLotExtensionAssociatedEvent(ParkingLotExtensionConfigEvent):
    name = 'parking_lot_extension_associated'
    routing_key = 'config.parkinglots.extensions.updated'


class ParkingLotExtensionDissociatedEvent(ParkingLotExtensionConfigEvent):
    name = 'parking_lot_extension_dissociated'
    routing_key = 'config.parkinglots.extensions.deleted'
