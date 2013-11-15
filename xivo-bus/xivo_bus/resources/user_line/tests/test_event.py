# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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


from ..event import UserLineConfigEvent


class ConcreteUserLineConfigEvent(UserLineConfigEvent):
    name = 'line_event'


USER_ID = 1
LINE_ID = 2
MAIN_USER = True
MAIN_LINE = True


class TestUserLineConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_id': USER_ID,
            'line_id': LINE_ID,
            'main_user': MAIN_USER,
            'main_line': MAIN_LINE
        }

    def test_marshal(self):
        command = ConcreteUserLineConfigEvent(USER_ID, LINE_ID, MAIN_USER, MAIN_LINE)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteUserLineConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('user_id', USER_ID),
            has_property('line_id', LINE_ID),
            has_property('main_user', MAIN_USER),
            has_property('main_line', MAIN_LINE)))
