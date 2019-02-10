# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid
from unittest import TestCase
from hamcrest import assert_that, equal_to

from .. import events


class AbstractEvent(events._BaseEvent):

    name = 'abstract_name_event'
    routing_key_fmt = 'abstract.routing_key.{uuid}'

    def __init__(self, body):
        self._body = body
        super(AbstractEvent, self).__init__()


class TestBaseEvent(TestCase):

    Event = AbstractEvent

    def setUp(self):
        self.user_uuid = uuid.uuid4()
        self.body = {'uuid': str(self.user_uuid), 'field': 'value'}

    def test_marshal(self):
        event = self.Event(self.body)
        assert_that(event.marshal(), equal_to(self.body))

    def test_unmarshal(self):
        event = self.Event.unmarshal(self.body)
        expected = self.Event(self.body)
        assert_that(event, equal_to(expected))
