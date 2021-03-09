# -*- coding: utf-8 -*-
# Copyright 2017-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from uuid import uuid4
from hamcrest import assert_that, equal_to


from ..event import GroupScheduleConfigEvent


class ConcreteGroupScheduleConfigEvent(GroupScheduleConfigEvent):
    name = 'trunk_endpoint_event'
    routing_key_fmt = 'config.groups.schedules.updated'


GROUP_ID = 1
GROUP_UUID = str(uuid4())
SCHEDULE_ID = 2


class TestGroupScheduleConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'group_id': GROUP_ID,
            'group_uuid': GROUP_UUID,
            'schedule_id': SCHEDULE_ID,
        }

    def test_marshal(self):
        command = ConcreteGroupScheduleConfigEvent(
            group_id=GROUP_ID,
            group_uuid=GROUP_UUID,
            schedule_id=SCHEDULE_ID,
        )

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteGroupScheduleConfigEvent.unmarshal(self.msg)

        assert_that(event._body, equal_to(self.msg))
