# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    has_entry,
    empty,
    is_,
    contains_exactly,
)

from .helpers import BusIntegrationTest


class TestHeaders(BusIntegrationTest):
    asset = 'headers'

    def test_event_binding(self):
        event = 'binding_test'

        with self.use_event(event):
            self.bus.publish(event, 'first payload')
        self.bus.publish(event, 'second payload')

        assert_that(self.bus.get_messages(event), contains_exactly('first payload'))

    def test_routing_key_disabled_with_headers_exchange(self):
        event = 'routing_key_event'
        key = 'events.good_key.#'

        with self.use_event(event, routing_key=key):
            self.bus.publish(event, 'message1', routing_key='events.good_key.here')
            self.bus.publish(event, 'message2', routing_key='events.wrong_key.here')

        assert_that(
            self.bus.get_messages(event), contains_exactly('message1', 'message2')
        )

    def test_bind_on_headers(self):
        event = 'bound_headers'
        headers = {'must_have': 'headers'}

        with self.use_event(event, headers=headers):
            self.bus.publish(event, {'some': 'payload'}, headers=headers)

        assert_that(
            self.bus.get_messages(event),
            contains_exactly((has_entry('some', 'payload'))),
        )

    def test_publish_without_expected_headers(self):
        event = 'no_publish_headers'
        headers = {'must_have': 'this'}

        with self.use_event(event, headers=headers):
            self.bus.publish(event, "payload")

        assert_that(self.bus.get_messages(event), is_(empty()))

    def test_publish_wrong_expected_headers_value(self):
        event = 'wrong_headers_value'
        headers = {'required': True}

        with self.use_event(event, headers=headers):
            self.bus.publish(event, "payload", headers={'required': False})

        assert_that(self.bus.get_messages(event), is_(empty()))

    def test_publish_ignore_extra_headers(self):
        event = 'extra_ignored_headers'
        headers = {'required': True}

        with self.use_event(event, headers=headers):
            self.bus.publish(
                event,
                {'some': 'payload'},
                headers={'required': True, 'other': 1, 'ignored': 'headers'},
            )

        assert_that(
            self.bus.get_messages(event),
            contains_exactly((has_entry('some', 'payload'))),
        )

    def test_multiple_events(self):
        event1, headers1 = 'event_1', {'headers': 1}
        event2, headers2 = 'event_2', {'headers': 2}
        event3, headers3 = 'event_3', {'headers': 3}

        with self.use_event(event1, headers1):
            with self.use_event(event2, headers2):
                with self.use_event(event3, headers3):
                    self.bus.publish(event1, 'payload1', headers1)
                    self.bus.publish(event2, 'payload2', headers2)
                    self.bus.publish(event3, 'payload3', headers3)

        assert_that(self.bus.get_messages(event1), contains_exactly('payload1'))
        assert_that(self.bus.get_messages(event2), contains_exactly('payload2'))
        assert_that(self.bus.get_messages(event3), contains_exactly('payload3'))

    def test_multiple_headers(self):
        event = 'test_event'
        headers1 = {'test': 1}
        headers2 = {'test': 2}
        headers3 = {'test': 3}
        headers4 = {'test': 4}

        with self.use_event(event, headers=headers1):
            with self.use_event(event, headers=headers2):
                with self.use_event(event, headers=headers3):
                    self.bus.publish(event, 'payload1', headers=headers1)
                    self.bus.publish(event, 'payload3', headers=headers3)
                    self.bus.publish(event, 'payload4', headers=headers4)

        assert_that(
            self.bus.get_messages(event), contains_exactly('payload1', 'payload3')
        )
