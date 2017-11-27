# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of

from ..event import OutcallCallPermissionConfigEvent


class ConcreteOutcallCallPermissionConfigEvent(OutcallCallPermissionConfigEvent):
    name = 'call_permission_event'


OUTCALL_ID = 1
CALL_PERMISSION_ID = 2


class TestOutcallCallPermissionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'outcall_id': OUTCALL_ID,
            'call_permission_id': CALL_PERMISSION_ID,
        }

    def test_marshal(self):
        command = ConcreteOutcallCallPermissionConfigEvent(OUTCALL_ID, CALL_PERMISSION_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteOutcallCallPermissionConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('outcall_id', OUTCALL_ID),
            has_property('call_permission_id', CALL_PERMISSION_ID)))
