# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_item, is_, empty

from .helpers import BusIntegrationTest


class TestRoutingKey(BusIntegrationTest):
    asset = 'topic'

    def test_bind_unbind(self):
        event = 'event_routing_key_bind'
        key = 'events.bus.bind_unbind_test'

        with self.local_event(event, routing_key=key):
            self.local_bus.publish(event, payload="first payload", routing_key=key)

        self.local_bus.publish(event, payload="second payload", routing_key=key)
        assert_that(self.local_messages(event), has_item("first payload"))

    def test_good_routing_key(self):
        event = 'event_good_routing_key'
        key = 'events.bus.good_key'

        with self.local_event(event, routing_key=key):
            self.local_bus.publish(event, payload="payload", routing_key=key)
        assert_that(self.local_messages(event), has_item("payload"))

    def test_wrong_routing_key(self):
        event = 'event_wrong_routing_key'
        key = 'events.bus.good_key'
        wrong_key = 'events.bus.wrong_key'

        with self.local_event(event, routing_key=key):
            self.local_bus.publish(event, payload="payload", routing_key=wrong_key)
        assert_that(self.local_messages(event), is_(empty()))

    def test_no_event_routing_key(self):
        event = 'event_no_key'
        key = 'events.bus.no_key'

        with self.local_event(event, routing_key=None):
            self.local_bus.publish(event, payload="payload", routing_key=key)
        assert_that(self.local_messages(event), is_(empty()))

    def test_no_routing_key(self):
        event = 'event_no_routing_key'
        key = ''

        with self.local_event(event, routing_key=key):
            self.local_bus.publish(event, payload="payload", routing_key=key)
        assert_that(self.local_messages(event), has_item("payload"))

    def test_headers_disabled_when_using_routing_key(self):
        event = 'headers_with_routing_key'
        key = 'events.bus.headers_test'

        with self.local_event(event, headers={'required': True}, routing_key=key):
            self.local_bus.publish(
                event, payload="payload", headers={'required': False}, routing_key=key
            )
        assert_that(self.local_messages(event), has_item("payload"))
