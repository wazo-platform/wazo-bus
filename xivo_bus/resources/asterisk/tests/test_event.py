# -*- coding: utf-8 -*-
# Copyright 2018-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid
import unittest

from hamcrest import assert_that, equal_to

from ..event import AsteriskReloadProgressEvent

ASTERISK_UUID = str(uuid.uuid4)
STATUS = 'starting'
COMMAND = 'core reload'
REQUEST_UUIDS = [
    'cf0a6633-be41-4fda-9ac9-3eef74b9ab88',
    '6b6b0456-8580-4476-89ea-250e8f555a93',
]


class TestUserVoicemailEvent(unittest.TestCase):
    def test_reload_routing_key_fmt(self):
        msg = AsteriskReloadProgressEvent(ASTERISK_UUID, STATUS, COMMAND, REQUEST_UUIDS)
        assert_that(
            msg.routing_key,
            equal_to('sysconfd.asterisk.reload.{}.{}'.format(ASTERISK_UUID, STATUS)),
        )
