# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import QueueScheduleConfigEvent


class ConcreteQueueScheduleConfigEvent(QueueScheduleConfigEvent):
    name = 'queue_schedule_event'


QUEUE_ID = 1
SCHEDULE_ID = 2


class TestQueueScheduleConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'queue_id': QUEUE_ID,
            'schedule_id': SCHEDULE_ID,
        }

    def test_marshal(self):
        command = ConcreteQueueScheduleConfigEvent(QUEUE_ID, SCHEDULE_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteQueueScheduleConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('queue_id', QUEUE_ID),
            has_property('schedule_id', SCHEDULE_ID)))
