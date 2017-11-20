# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


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

        assert_that(event, all_of(
            has_property('user_id', USER_ID),
            has_property('cti_profile_id', CTI_PROFILE_ID),
            has_property('enabled', True)))
