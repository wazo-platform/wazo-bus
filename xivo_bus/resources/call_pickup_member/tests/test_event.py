# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import (
    CallPickupInterceptorGroupsAssociatedEvent,
    CallPickupInterceptorUsersAssociatedEvent,
)


CALL_PICKUP_ID = 5
GROUP_IDS = [1, 2, 3]
USER_UUIDS = ['abcd-123', 'efg-456', 'hij-789']


class TestCallPickupUserConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'call_pickup_id': CALL_PICKUP_ID,
            'user_uuids': USER_UUIDS,
        }

    def test_marshal(self):
        command = CallPickupInterceptorUsersAssociatedEvent(CALL_PICKUP_ID, USER_UUIDS)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = CallPickupInterceptorUsersAssociatedEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('call_pickup_id', CALL_PICKUP_ID),
            has_property('user_uuids', USER_UUIDS),
        ))


class TestCallPickupGroupConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'call_pickup_id': CALL_PICKUP_ID,
            'group_ids': GROUP_IDS,
        }

    def test_marshal(self):
        command = CallPickupInterceptorGroupsAssociatedEvent(CALL_PICKUP_ID, GROUP_IDS)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = CallPickupInterceptorGroupsAssociatedEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('call_pickup_id', CALL_PICKUP_ID),
            has_property('group_ids', GROUP_IDS),
        ))
