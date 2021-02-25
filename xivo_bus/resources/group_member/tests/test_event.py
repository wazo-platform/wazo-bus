# -*- coding: utf-8 -*-
# Copyright 2016-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from uuid import uuid4
from hamcrest import assert_that, equal_to


from ..event import GroupMemberUsersAssociatedEvent, GroupMemberExtensionsAssociatedEvent


GROUP_ID = 5
GROUP_UUID = str(uuid4())
USER_UUIDS = ['abcd-123', 'efg-456', 'hij-789']
EXTENSIONS = [{'exten': '123', 'context': 'default'}, {'exten': '456', 'context': 'default2'}]


class TestGroupMemberUserConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'group_id': GROUP_ID,
            'group_uuid': GROUP_UUID,
            'user_uuids': USER_UUIDS,
        }

    def test_marshal(self):
        command = GroupMemberUsersAssociatedEvent(
            group_id=GROUP_ID,
            group_uuid=GROUP_UUID,
            user_uuids=USER_UUIDS,
        )

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = GroupMemberUsersAssociatedEvent.unmarshal(self.msg)

        assert_that(event._body, equal_to(self.msg))


class TestGroupMemberExtensionConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'group_id': GROUP_ID,
            'group_uuid': GROUP_UUID,
            'extensions': EXTENSIONS,
        }

    def test_marshal(self):
        event = GroupMemberExtensionsAssociatedEvent(
            group_id=GROUP_ID,
            group_uuid=GROUP_UUID,
            extensions=EXTENSIONS,
        )

        msg = event.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = GroupMemberExtensionsAssociatedEvent.unmarshal(self.msg)

        assert_that(event._body, equal_to(self.msg))
