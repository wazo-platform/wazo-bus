# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
from hamcrest import assert_that, equal_to, has_property, all_of


from ..event import PagingMemberUsersAssociatedEvent


GROUP_ID = 5
USER_UUIDS = ['abcd-123', 'efg-456', 'hij-789']


class TestPagingMemberUserConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'paging_id': GROUP_ID,
            'user_uuids': USER_UUIDS,
        }

    def test_marshal(self):
        command = PagingMemberUsersAssociatedEvent(GROUP_ID, USER_UUIDS)

        msg = command.marshal()

        assert_that(msg, equal_to(self.msg))

    def test_unmarshal(self):
        event = PagingMemberUsersAssociatedEvent.unmarshal(self.msg)

        assert_that(event, all_of(
            has_property('paging_id', GROUP_ID),
            has_property('user_uuids', USER_UUIDS)))
