# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import uuid
import unittest

from hamcrest import assert_that, equal_to

from ..events import (
    PresenceUpdatedEvent,
)

USER_UUID = str(uuid.uuid4())
USER = {'uuid': USER_UUID}


class TestPresenceEvent(unittest.TestCase):

    def test_updated_routing_key_fmt(self):
        msg = PresenceUpdatedEvent(USER)
        assert_that(
            msg.routing_key,
            equal_to('chatd.users.{}.presences.updated'.format(USER_UUID))
        )
