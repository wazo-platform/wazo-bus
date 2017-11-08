# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import TrunkEndpointConfigEvent


class ConcreteTrunkEndpointConfigEvent(TrunkEndpointConfigEvent):
    name = 'trunk_endpoint_event'


TRUNK_ID = 1
ENDPOINT_ID = 2


class TestTrunkEndpointConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'trunk_id': TRUNK_ID,
            'endpoint_id': ENDPOINT_ID,
        }

    def test_marshal(self):
        command = ConcreteTrunkEndpointConfigEvent(TRUNK_ID, ENDPOINT_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteTrunkEndpointConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('trunk_id', TRUNK_ID),
            has_property('endpoint_id', ENDPOINT_ID)))
