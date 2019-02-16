# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to

from ..event import UserCtiProfileEditedEvent

USER_ID = 1
CTI_PROFILE_ID = 2


class TestUserVoicemailEvent(unittest.TestCase):

    def test_edited_routing_key_fmt(self):
        msg = UserCtiProfileEditedEvent(USER_ID, CTI_PROFILE_ID, enabled=True)
        assert_that(
            msg.routing_key,
            equal_to('config.user_cti_profile_association.edited')
        )
