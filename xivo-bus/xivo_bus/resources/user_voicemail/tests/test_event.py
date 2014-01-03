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
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import UserVoicemailConfigEvent


class ConcreteUserVoicemailConfigEvent(UserVoicemailConfigEvent):
    name = 'voicemail_event'


USER_ID = 1
VOICEMAIL_ID = 2
ENABLED = True


class TestUserVoicemailConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_id': USER_ID,
            'voicemail_id': VOICEMAIL_ID,
            'enabled': ENABLED
        }

    def test_marshal(self):
        command = ConcreteUserVoicemailConfigEvent(USER_ID, VOICEMAIL_ID, ENABLED)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteUserVoicemailConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('user_id', USER_ID),
            has_property('voicemail_id', VOICEMAIL_ID),
            has_property('enabled', ENABLED)))
