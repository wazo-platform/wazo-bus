# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import UserGroupsAssociatedEvent


USER_UUID = 'abcd-123'
GROUP_IDS = [2, 4, 7]


class TestUserGroupConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_uuid': USER_UUID,
            'group_ids': GROUP_IDS,
        }

    def test_marshal(self):
        command = UserGroupsAssociatedEvent(USER_UUID, GROUP_IDS)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = UserGroupsAssociatedEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('user_uuid', USER_UUID),
            has_property('group_ids', GROUP_IDS)))
