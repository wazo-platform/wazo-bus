# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_entry, empty, is_, contains_exactly
from .helpers import BusIntegrationTest


class TestHeaders(BusIntegrationTest):
    asset = 'headers'

    def test_event_binding(self):
        event = 'binding_test'
        headers = {'name': event}

        with self.local_event(event):
            self.local_bus.publish(event, headers=headers, payload='first payload')
        self.local_bus.publish(event, headers=headers, payload='second payload')

        assert_that(self.local_messages(event), contains_exactly('first payload'))

    def test_routing_key_disabled_with_headers_exchange(self):
        event = 'routing_key_event'
        key = 'events.good_key.#'
        headers = {'name': event}

        with self.local_event(event, routing_key=key):
            self.local_bus.publish(
                event,
                headers=headers,
                payload='message1',
                routing_key='events.good_key.here',
            )
            self.local_bus.publish(
                event,
                headers=headers,
                payload='message2',
                routing_key='events.wrong_key.here',
            )

        assert_that(
            self.local_messages(event), contains_exactly('message1', 'message2')
        )

    def test_bind_on_headers(self):
        event = 'bound_headers'
        headers = {'name': event, 'must_have': 'headers'}

        with self.local_event(event, headers=headers):
            self.local_bus.publish(event, payload={'some': 'payload'}, headers=headers)

        assert_that(
            self.local_messages(event), contains_exactly((has_entry('some', 'payload')))
        )

    def test_publish_without_expected_headers(self):
        event = 'no_publish_headers'
        headers = {'name': event, 'must_have': 'this'}

        with self.local_event(event, headers=headers):
            self.local_bus.publish(event, payload="payload", headers={'name': event})

        assert_that(self.local_messages(event), is_(empty()))

    def test_publish_wrong_expected_headers_value(self):
        event = 'wrong_headers_value'
        headers = {'name': event, 'required': True}

        with self.local_event(event, headers=headers):
            self.local_bus.publish(
                event, payload="payload", headers={'name': event, 'required': False}
            )

        assert_that(self.local_messages(event), is_(empty()))

    def test_publish_ignore_extra_headers(self):
        event = 'extra_ignored_headers'
        headers = {'name': event, 'required': True}

        with self.local_event(event, headers=headers):
            self.local_bus.publish(
                event,
                payload={'some': 'payload'},
                headers={
                    'name': event,
                    'required': True,
                    'other': 1,
                    'ignored': 'headers',
                },
            )

        assert_that(
            self.local_messages(event), contains_exactly((has_entry('some', 'payload')))
        )

    def test_multiple_events(self):
        event1, headers1 = 'event_1', {'headers': 1}
        event2, headers2 = 'event_2', {'headers': 2}
        event3, headers3 = 'event_3', {'headers': 3}

        with self.local_event(event1, headers1):
            with self.local_event(event2, headers2):
                with self.local_event(event3, headers3):
                    self.local_bus.publish(event1, payload='payload1', headers=headers1)
                    self.local_bus.publish(event2, payload='payload2', headers=headers2)
                    self.local_bus.publish(event3, payload='payload3', headers=headers3)

        assert_that(self.local_messages(event1), contains_exactly('payload1'))
        assert_that(self.local_messages(event2), contains_exactly('payload2'))
        assert_that(self.local_messages(event3), contains_exactly('payload3'))

    def test_multiple_headers(self):
        event = 'test_event'
        headers1 = {'test': 1}
        headers2 = {'test': 2}
        headers3 = {'test': 3}
        headers4 = {'test': 4}

        with self.local_event(event, headers=headers1):
            with self.local_event(event, headers=headers2):
                with self.local_event(event, headers=headers3):
                    self.local_bus.publish(event, payload='payload1', headers=headers1)
                    self.local_bus.publish(event, payload='payload3', headers=headers3)
                    self.local_bus.publish(event, payload='payload4', headers=headers4)

        assert_that(
            self.local_messages(event), contains_exactly('payload1', 'payload3')
        )

    def test_remote_bus_publish_local(self):
        event = 'multibus_test_local_pl'
        headers = {'name': event}

        with self.remote_event(event, headers=headers):
            self.local_bus.publish(event, headers=headers, payload="local payload")
        assert_that(self.remote_messages(event), contains_exactly("local payload"))

    def test_local_bus_publish_remote(self):
        event = 'multibus_test_local_pr'
        headers = {'name': event}

        with self.local_event(event, headers=headers):
            self.remote_bus.publish(event, "remote payload", headers=headers)
        assert_that(self.local_messages(event), contains_exactly("remote payload"))

    def test_remote_bus_publish_remote(self):
        event = 'multibus_test_remote_pl'
        headers = {'name': event}

        with self.remote_event(event, headers=headers):
            self.remote_bus.publish(event, "remote payload", headers=headers)
        assert_that(self.remote_messages(event), contains_exactly("remote payload"))
