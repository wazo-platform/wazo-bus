# -*- coding: utf-8 -*-

# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0+

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
