# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_entries


from ..event import UserCtiProfileConfigEvent


class ConcreteUserCtiProfileConfigEvent(UserCtiProfileConfigEvent):
    name = 'cti_profile_event'


USER_ID = 1
CTI_PROFILE_ID = 2


class TestUserCtiProfileEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_id': USER_ID,
            'cti_profile_id': CTI_PROFILE_ID,
            'enabled': True
        }

    def test_marshal(self):
        command = ConcreteUserCtiProfileConfigEvent(USER_ID, CTI_PROFILE_ID, True)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteUserCtiProfileConfigEvent.unmarshal(self.msg)

        assert_that(event._body, has_entries(
            user_id=USER_ID,
            cti_profile_id=CTI_PROFILE_ID,
            enabled=True
        ))
