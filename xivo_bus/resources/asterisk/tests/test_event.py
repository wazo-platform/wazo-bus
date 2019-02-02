# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid
from unittest import TestCase
from hamcrest import assert_that, equal_to

from ..event import AsteriskReloadProgressEvent


class _BaseTestCase(TestCase):

    def setUp(self):
        self.uuid = str(uuid.uuid4())
        self.status = 'starting'
        self.command = 'core reload'
        self.body = {'uuid': self.uuid, 'status': self.status, 'command': self.command}

    def test_marshal(self):
        event = self.Event(self.uuid, self.status, self.command)
        assert_that(event.marshal(), equal_to(self.body))

    def test_unmarshal(self):
        event = self.Event.unmarshal(self.body)
        expected = self.Event(self.uuid, self.status, self.command)
        assert_that(event, equal_to(expected))


class TestAsteriskReloadProgressEvent(_BaseTestCase):

    Event = AsteriskReloadProgressEvent
