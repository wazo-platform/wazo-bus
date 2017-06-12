# -*- coding: utf-8 -*-

# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

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
