# -*- coding: utf-8 -*-

# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

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
