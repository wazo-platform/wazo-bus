# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import unittest
import uuid

from hamcrest import assert_that
from hamcrest import equal_to

from ..event import AgentStatusUpdateEvent
from ..event import CallFormResultEvent
from ..event import EndpointStatusUpdateEvent


SOME_UUID = str(uuid.uuid4())


class TestCallFormResultEvent(unittest.TestCase):

    def test_marshal(self):
        user_id = 42
        variables = {'a': 'b'}
        event = CallFormResultEvent(user_id, variables)

        msg = event.marshal()

        assert_that(msg, equal_to({'user_id': 42,
                                   'variables': {'a': 'b'}}))

    def test_string_user_id(self):
        user_id = "42"

        event = CallFormResultEvent(user_id, {})

        assert_that(event.user_id, equal_to(42))


class TestAgentStatusUpdateEvent(unittest.TestCase):

    def test_marshal(self):
        agent_id = 42
        status = 'logged_in'

        event = AgentStatusUpdateEvent(agent_id, status)
        msg = event.marshal()

        assert_that(msg, equal_to({'agent_id': 42,
                                   'status': 'logged_in'}))

    def test_that_string_ids_are_not_leaked(self):
        agent_id = '42'
        status = 'logged_in'

        event = AgentStatusUpdateEvent(agent_id, status)
        msg = event.marshal()

        assert_that(msg, equal_to({'agent_id': 42,
                                   'status': 'logged_in'}))


class TestEndpointStatusUpdateEvent(unittest.TestCase):

    def test_marshal(self):
        endpoint_id = 42
        status = 8

        event = EndpointStatusUpdateEvent(endpoint_id, status)
        msg = event.marshal()

        assert_that(msg, equal_to({'endpoint_id': endpoint_id,
                                   'status': status}))

    def test_marshal_with_string_status(self):
        endpoint_id = 42

        event = EndpointStatusUpdateEvent(endpoint_id, '8')
        msg = event.marshal()

        assert_that(msg, equal_to({'endpoint_id': endpoint_id,
                                   'status': 8}))

    def test_that_string_endpoint_ids_are_not_leaked(self):
        endpoint_id = '42'
        status = 8

        event = EndpointStatusUpdateEvent(endpoint_id, status)

        msg = event.marshal()

        assert_that(msg, equal_to({'endpoint_id': 42,
                                   'status': status}))
