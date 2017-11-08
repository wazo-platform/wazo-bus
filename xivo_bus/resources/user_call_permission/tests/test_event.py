# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import UserCallPermissionConfigEvent


class ConcreteUserCallPermissionConfigEvent(UserCallPermissionConfigEvent):
    name = 'call_permission_event'


USER_UUID = 'abcd-1234'
CALL_PERMISSION_ID = 2


class TestUserCallPermissionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_uuid': USER_UUID,
            'call_permission_id': CALL_PERMISSION_ID,
        }

    def test_marshal(self):
        command = ConcreteUserCallPermissionConfigEvent(USER_UUID, CALL_PERMISSION_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteUserCallPermissionConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('user_uuid', USER_UUID),
            has_property('call_permission_id', CALL_PERMISSION_ID)))
