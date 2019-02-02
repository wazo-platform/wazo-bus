# -*- coding: utf-8 -*-
# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from uuid import uuid4
from hamcrest import assert_that, equal_to
from ..event import FavoriteAddedEvent, FavoriteDeletedEvent


def uuid():
    return str(uuid4())


class TestFavoriteAddedEvent(unittest.TestCase):

    def setUp(self):
        self.xivo_uuid, self.user_uuid = uuid(), uuid()
        self.source, self.source_entry_id = 'internal', uuid()
        self.event = FavoriteAddedEvent(
            self.xivo_uuid, self.user_uuid, self.source, self.source_entry_id)

    def marshal(self):
        payload = self.event.marshal()

        expected_payload = {
            'xivo_uuid': self.xivo_uuid,
            'user_uuid': self.user_uuid,
            'source': self.source,
            'source_entry_id': self.source_entry_id,
        }
        assert_that(payload, equal_to(expected_payload))

    def test_routing_key(self):
        routing_key = self.event.routing_key
        expected_routing_key = 'directory.{}.favorite.created'.format(self.user_uuid)

        assert_that(routing_key, equal_to(expected_routing_key))

    def test_required_acl(self):
        required_acl = self.event.required_acl
        expected_required_acl = 'events.directory.{}.favorite.created'.format(self.user_uuid)

        assert_that(required_acl, equal_to(expected_required_acl))


class TestFavoriteDeletedEvent(unittest.TestCase):

    def setUp(self):
        self.xivo_uuid, self.user_uuid = uuid(), uuid()
        self.source, self.source_entry_id = 'internal', uuid()
        self.event = FavoriteDeletedEvent(
            self.xivo_uuid, self.user_uuid, self.source, self.source_entry_id)

    def marshal(self):
        payload = self.event.marshal()

        expected_payload = {
            'xivo_uuid': self.xivo_uuid,
            'user_uuid': self.user_uuid,
            'source': self.source,
            'source_entry_id': self.source_entry_id,
        }
        assert_that(payload, equal_to(expected_payload))

    def test_routing_key(self):
        routing_key = self.event.routing_key
        expected_routing_key = 'directory.{}.favorite.deleted'.format(self.user_uuid)

        assert_that(routing_key, equal_to(expected_routing_key))

    def test_required_acl(self):
        required_acl = self.event.required_acl
        expected_required_acl = 'events.directory.{}.favorite.deleted'.format(self.user_uuid)

        assert_that(required_acl, equal_to(expected_required_acl))
