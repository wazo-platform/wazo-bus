# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import GroupScheduleConfigEvent


class ConcreteGroupScheduleConfigEvent(GroupScheduleConfigEvent):
    name = 'trunk_endpoint_event'


GROUP_ID = 1
SCHEDULE_ID = 2


class TestGroupScheduleConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'group_id': GROUP_ID,
            'schedule_id': SCHEDULE_ID,
        }

    def test_marshal(self):
        command = ConcreteGroupScheduleConfigEvent(GROUP_ID, SCHEDULE_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteGroupScheduleConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('group_id', GROUP_ID),
            has_property('schedule_id', SCHEDULE_ID)))
