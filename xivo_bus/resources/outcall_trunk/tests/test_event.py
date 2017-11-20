# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import OutcallTrunksAssociatedEvent


OUTCALL_ID = 'abcd-1234'
TRUNK_IDS = [1, 3, 2, 4, 6]


class TestOutcallTrunkConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'outcall_id': OUTCALL_ID,
            'trunk_ids': TRUNK_IDS,
        }

    def test_marshal(self):
        command = OutcallTrunksAssociatedEvent(OUTCALL_ID, TRUNK_IDS)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = OutcallTrunksAssociatedEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('outcall_id', OUTCALL_ID),
            has_property('trunk_ids', TRUNK_IDS)))
