# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to

from ..event import ResourceConfigEvent, BaseEvent


class AbstractEvent(BaseEvent):

    name = 'abstract_name_event'
    routing_key_fmt = 'abstract.routing_key.{id}'

    def __init__(self, **body):
        self._body = body
        super(AbstractEvent, self).__init__()


class TestBaseEvent(unittest.TestCase):

    Event = AbstractEvent

    def setUp(self):
        self.user_id = 2
        self.body = {'id': self.user_id, 'field': 'value'}

    def test_marshal(self):
        event = self.Event(**self.body)
        assert_that(event.marshal(), equal_to(self.body))

    def test_unmarshal(self):
        event = self.Event.unmarshal(self.body)
        expected = self.Event(**self.body)
        assert_that(event, equal_to(expected))


class ConcreteResourceConfigEvent(ResourceConfigEvent):

    name = 'foo'


RESOURCE_ID = 42


class TestResourceConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {'id': RESOURCE_ID}

    def test_marshal(self):
        command = ConcreteResourceConfigEvent(RESOURCE_ID)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteResourceConfigEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteResourceConfigEvent.name)
        self.assertEqual(command.id, RESOURCE_ID)
