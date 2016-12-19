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

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import ParkingLotExtensionConfigEvent


class ConcreteParkingLotExtensionConfigEvent(ParkingLotExtensionConfigEvent):
    name = 'trunk_endpoint_event'


PARKING_LOT_ID = 1
EXTENSION_ID = 2


class TestParkingLotExtensionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'parking_lot_id': PARKING_LOT_ID,
            'extension_id': EXTENSION_ID,
        }

    def test_marshal(self):
        command = ConcreteParkingLotExtensionConfigEvent(PARKING_LOT_ID, EXTENSION_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteParkingLotExtensionConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('parking_lot_id', PARKING_LOT_ID),
            has_property('extension_id', EXTENSION_ID)))
