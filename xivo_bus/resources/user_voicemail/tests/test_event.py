# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to

from ..event import (
    UserVoicemailAssociatedEvent,
    UserVoicemailDissociatedEvent,
)

USER_UUID = 'abcd-1234'
VOICEMAIL_ID = 2


class TestUserVoicemailEvent(unittest.TestCase):

    def test_associated_routing_key_fmt(self):
        msg = UserVoicemailAssociatedEvent(USER_UUID, VOICEMAIL_ID)
        assert_that(
            msg.routing_key,
            equal_to('config.users.{}.voicemails.updated'.format(USER_UUID))
        )

    def test_dissociated_routing_key_fmt(self):
        msg = UserVoicemailDissociatedEvent(USER_UUID, VOICEMAIL_ID)
        assert_that(
            msg.routing_key,
            equal_to('config.users.{}.voicemails.deleted'.format(USER_UUID))
        )
