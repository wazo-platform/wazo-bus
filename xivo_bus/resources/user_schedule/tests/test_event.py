# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of

from ..event import UserScheduleConfigEvent


class ConcreteUserScheduleConfigEvent(UserScheduleConfigEvent):
    name = 'trunk_endpoint_event'


USER_UUID = 'abcde-1234'
SCHEDULE_ID = 2


class TestUserScheduleConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_uuid': USER_UUID,
            'schedule_id': SCHEDULE_ID,
        }

    def test_marshal(self):
        command = ConcreteUserScheduleConfigEvent(USER_UUID, SCHEDULE_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteUserScheduleConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('user_uuid', USER_UUID),
            has_property('schedule_id', SCHEDULE_ID)))
