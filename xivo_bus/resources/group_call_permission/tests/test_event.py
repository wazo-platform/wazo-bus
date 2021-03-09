# -*- coding: utf-8 -*-
# Copyright 2017-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_properties

from ..event import GroupCallPermissionConfigEvent


class ConcreteGroupCallPermissionConfigEvent(GroupCallPermissionConfigEvent):
    name = 'call_permission_event'
    routing_key_fmt = 'config.groups.{group_uuid}.callpermissions'


GROUP_ID = 1
CALL_PERMISSION_ID = 2
GROUP_UUID = 'b60a25ce-f6ab-4fbb-b30b-8b20ad347f36'


class TestGroupCallPermissionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'group_id': GROUP_ID,
            'call_permission_id': CALL_PERMISSION_ID,
            'group_uuid': GROUP_UUID,
        }

    def test_marshal(self):
        event = ConcreteGroupCallPermissionConfigEvent(
            group_id=GROUP_ID,
            group_uuid=GROUP_UUID,
            call_permission_id=CALL_PERMISSION_ID,
        )

        msg = event.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = ConcreteGroupCallPermissionConfigEvent.unmarshal(self.msg)

        assert_that(event, has_properties(_body=self.msg))
