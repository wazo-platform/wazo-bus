# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import uuid
import unittest

from hamcrest import assert_that, equal_to

from ..events import (
    PresenceUpdatedEvent,
    UserRoomCreatedEvent,
    UserRoomMessageCreatedEvent,
)

USER_UUID = str(uuid.uuid4())
ROOM_UUID = str(uuid.uuid4())
USER = {'uuid': USER_UUID}
ROOM = {}
MESSAGE = {}


class TestPresenceEvent(unittest.TestCase):

    def test_updated_routing_key_fmt(self):
        msg = PresenceUpdatedEvent(USER)
        assert_that(
            msg.routing_key,
            equal_to('chatd.users.{}.presences.updated'.format(USER_UUID))
        )


class TestRoomEvent(unittest.TestCase):

    def test_updated_routing_key_fmt(self):
        msg = UserRoomCreatedEvent(USER_UUID, ROOM)
        assert_that(
            msg.routing_key,
            equal_to('chatd.users.{}.rooms.created'.format(USER_UUID))
        )


class TestUserRoomMessageCreatedEvent(unittest.TestCase):

    def test_updated_routing_key_fmt(self):
        msg = UserRoomMessageCreatedEvent(USER_UUID, ROOM_UUID, MESSAGE)
        assert_that(
            msg.routing_key,
            equal_to('chatd.users.{}.rooms.{}.messages.created'.format(USER_UUID, ROOM_UUID))
        )
