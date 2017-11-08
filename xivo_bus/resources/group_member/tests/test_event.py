# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique Inc.
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import GroupMemberUsersAssociatedEvent


GROUP_ID = 5
USER_UUIDS = ['abcd-123', 'efg-456', 'hij-789']


class TestGroupMemberUserConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'group_id': GROUP_ID,
            'user_uuids': USER_UUIDS,
        }

    def test_marshal(self):
        command = GroupMemberUsersAssociatedEvent(GROUP_ID, USER_UUIDS)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = GroupMemberUsersAssociatedEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('group_id', GROUP_ID),
            has_property('user_uuids', USER_UUIDS)))
