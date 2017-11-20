# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import UserEntityConfigEvent


class ConcreteUserEntityConfigEvent(UserEntityConfigEvent):
    name = 'entity_event'


USER_UUID = 'abcd-1234'
ENTITY_ID = 2


class TestUserEntityConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_uuid': USER_UUID,
            'entity_id': ENTITY_ID,
        }

    def test_marshal(self):
        command = ConcreteUserEntityConfigEvent(USER_UUID, ENTITY_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteUserEntityConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('user_uuid', USER_UUID),
            has_property('entity_id', ENTITY_ID)))
