# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid
from unittest import TestCase
from hamcrest import assert_that, equal_to
from .. import events


class _BaseTestCase:

    def setUp(self):
        self.user_uuid = uuid.uuid4()
        self.external_auth_name = 'zoho'
        self.body = {'user_uuid': str(self.user_uuid), 'external_auth_name': self.external_auth_name}

    def test_marshal(self):
        event = self.Event(self.user_uuid, self.external_auth_name)
        assert_that(event.marshal(), equal_to(self.body))

    def test_unmarshal(self):
        event = self.Event.unmarshal(self.body)
        expected = self.Event(self.user_uuid, self.external_auth_name)
        assert_that(event, equal_to(expected))


class TestUserExternalAuthAddedEvent(_BaseTestCase, TestCase):

    Event = events.UserExternalAuthAdded


class TestUserExternalAuthAuthorizedEvent(_BaseTestCase, TestCase):

    Event = events.UserExternalAuthAuthorized


class TestUserExternalAuthDeletedEvent(_BaseTestCase, TestCase):

    Event = events.UserExternalAuthDeleted
