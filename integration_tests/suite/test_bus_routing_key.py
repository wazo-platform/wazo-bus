# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_item, is_, empty

from .helpers import BusIntegrationTest


class TestRoutingKey(BusIntegrationTest):
    asset = 'topic'

    def test_bind_unbind(self):
        event = 'event_routing_key_bind'
        key = 'events.bus.bind_unbind_test'

        with self.use_event(event, routing_key=key):
            self.bus.publish(event, "first payload", routing_key=key)

        self.bus.publish(event, "second payload", routing_key=key)
        assert_that(self.bus.get_messages(event), has_item("first payload"))

    def test_good_routing_key(self):
        event = 'event_good_routing_key'
        key = 'events.bus.good_key'

        with self.use_event(event, routing_key=key):
            self.bus.publish(event, "payload", routing_key=key)
        assert_that(self.bus.get_messages(event), has_item("payload"))

    def test_wrong_routing_key(self):
        event = 'event_wrong_routing_key'
        key = 'events.bus.good_key'
        wrong_key = 'events.bus.wrong_key'

        with self.use_event(event, routing_key=key):
            self.bus.publish(event, "payload", routing_key=wrong_key)
        assert_that(self.bus.get_messages(event), is_(empty()))

    def test_no_publish_routing_key(self):
        event = 'event_publish_null_routing_key'
        key = 'events.bus.some_key'

        with self.use_event(event, routing_key=key):
            self.bus.publish(event, "payload", routing_key=None)
        assert_that(self.bus.get_messages(event), is_(empty()))

    def test_no_event_routing_key(self):
        event = 'event_no_key'
        key = 'events.bus.no_key'

        with self.use_event(event, routing_key=None):
            self.bus.publish(event, "payload", routing_key=key)
        assert_that(self.bus.get_messages(event), is_(empty()))

    def test_no_routing_key(self):
        event = 'event_no_routing_key'
        key = ''

        with self.use_event(event, routing_key=key):
            self.bus.publish(event, "payload", routing_key=key)
        assert_that(self.bus.get_messages(event), has_item("payload"))

    def test_headers_disabled_with_routing_key(self):
        event = 'headers_with_routing_key'
        key = 'events.bus.headers_test'

        with self.use_event(event, headers={'required': True}, routing_key=key):
            self.bus.publish(
                event, "payload", headers={'required': False}, routing_key=key
            )
        assert_that(self.bus.get_messages(event), has_item("payload"))
