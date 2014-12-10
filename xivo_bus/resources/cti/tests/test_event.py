# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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
from ..event import CallFormResultEvent
from ..event import UserStatusUpdateEvent
from hamcrest import assert_that
from hamcrest import equal_to


class TestCallFormResultEvent(unittest.TestCase):

    def test_marshal(self):
        user_id = 42
        variables = {'a': 'b'}
        event = CallFormResultEvent(user_id, variables)

        msg = event.marshal()

        assert_that(msg, equal_to({'user_id': 42,
                                   'variables': {'a': 'b'}}))

    def test_string_user_id(self):
        user_id = "42"

        event = CallFormResultEvent(user_id, {})

        assert_that(event.user_id, equal_to(42))


class TestUserStatusUpdateEvent(unittest.TestCase):

    def test_marchal(self):
        user_id = 42
        status = 'busy'

        event = UserStatusUpdateEvent(user_id, status)

        msg = event.marshal()

        assert_that(msg, equal_to({'user_id': 42,
                                   'status': status}))

    def test_that_string_user_ids_are_not_leaked(self):
        user_id = '42'
        status = 'busy'

        event = UserStatusUpdateEvent(user_id, status)

        msg = event.marshal()

        assert_that(msg, equal_to({'user_id': 42,
                                   'status': status}))
