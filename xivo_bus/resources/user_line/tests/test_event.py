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
USER_ID = 1
LINE_ID = 2
MAIN_USER = True
MAIN_LINE = True
TENANT_UUID = str(uuid.uuid4())


class TestUserLineEvent(unittest.TestCase):

    def test_associated_routing_key_fmt(self):
        msg = UserLineAssociatedEvent(
            USER_UUID,
            USER_ID,
            LINE_ID,
            MAIN_USER,
            MAIN_LINE,
            TENANT_UUID,
        )
        assert_that(
            msg.routing_key,
            equal_to('config.user_line_association.created')
        )

    def test_dissociated_routing_key_fmt(self):
        msg = UserLineDissociatedEvent(
            USER_UUID,
            USER_ID,
            LINE_ID,
            MAIN_USER,
            MAIN_LINE,
            TENANT_UUID,
        )
        assert_that(
            msg.routing_key,
            equal_to('config.user_line_association.deleted')
        )
