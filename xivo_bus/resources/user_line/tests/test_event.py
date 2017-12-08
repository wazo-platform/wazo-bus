# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_entries


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

        assert_that(event._body, has_entries(
            user_id=USER_ID,
            line_id=LINE_ID,
            main_user=MAIN_USER,
            main_line=MAIN_LINE
        ))
