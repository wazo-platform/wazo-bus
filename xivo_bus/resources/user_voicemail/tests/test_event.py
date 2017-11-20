# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import UserVoicemailConfigEvent


class ConcreteUserVoicemailConfigEvent(UserVoicemailConfigEvent):
    name = 'voicemail_event'


USER_UUID = 'abcd-1234'
VOICEMAIL_ID = 2


class TestUserVoicemailConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'user_uuid': USER_UUID,
            'voicemail_id': VOICEMAIL_ID,
        }

    def test_marshal(self):
        command = ConcreteUserVoicemailConfigEvent(USER_UUID, VOICEMAIL_ID)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteUserVoicemailConfigEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('user_uuid', USER_UUID),
            has_property('voicemail_id', VOICEMAIL_ID)))
