# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import uuid
import unittest

from hamcrest import assert_that, equal_to

from ..event import (
    UserLineAssociatedEvent,
    UserLineDissociatedEvent,
)

USER_UUID = str(uuid.uuid4())
USER = {'uuid': USER_UUID}
LINE_ID = 2
LINE = {'id': LINE_ID}
MAIN_USER = True
MAIN_LINE = True


class TestUserLineEvent(unittest.TestCase):

    def test_associated_routing_key_fmt(self):
        msg = UserLineAssociatedEvent(USER, LINE, MAIN_USER, MAIN_LINE)
        assert_that(
            msg.routing_key,
            equal_to('config.users.{}.lines.{}.updated'.format(USER_UUID, LINE_ID))
        )

    def test_dissociated_routing_key_fmt(self):
        msg = UserLineDissociatedEvent(USER, LINE, MAIN_USER, MAIN_LINE)
        assert_that(
            msg.routing_key,
            equal_to('config.users.{}.lines.{}.deleted'.format(USER_UUID, LINE_ID))
        )
