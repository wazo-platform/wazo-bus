# -*- coding: utf-8 -*-
# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid
import unittest

from hamcrest import assert_that, equal_to

from ..event import AsteriskReloadProgressEvent

ASTERISK_UUID = str(uuid.uuid4)
STATUS = 'starting'
COMMAND = 'core reload'


class TestUserVoicemailEvent(unittest.TestCase):

    def test_reload_routing_key_fmt(self):
        msg = AsteriskReloadProgressEvent(ASTERISK_UUID, STATUS, COMMAND)
        assert_that(
            msg.routing_key,
            equal_to('sysconfd.asterisk.reload.{}.{}'.format(ASTERISK_UUID, STATUS))
        )
