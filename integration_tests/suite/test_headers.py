# Copyright 2021-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime
from hamcrest import (
    assert_that,
    has_entry,
    has_entries,
    has_key,
    has_items,
    has_item,
    empty,
    is_,
    has_length,
)
from .helpers.base import BusIntegrationTest
from .helpers.events import MockEvent


class TestHeaders(BusIntegrationTest):
    asset = 'headers'

    def test_event_binding(self):
        event_name = 'binding_test'
        event1 = MockEvent(event_name, value='first payload')
        event2 = MockEvent(event_name, value='second payload')

        with self.local_event(event_name):
            self.local_bus.publish(event1)
            assert_that(
                self.local_messages(event_name, 1),
                has_item(has_entry('value', 'first payload')),
            )

        self.local_bus.publish(event2)
        assert_that(self.local_messages(event_name, 1), is_(empty()))

    def test_routing_key_disabled_with_headers_exchange(self):
        event_name = 'routing_key_event'
        event1 = MockEvent(event_name, value='first value')
        event2 = MockEvent(event_name, value='second value')

        with self.local_event(event_name, routing_key='events.good_key.#'):
            self.local_bus.publish(event1, routing_key='events.good_key.1')
            self.local_bus.publish(event2, routing_key='events.wrong_key.1')

            assert_that(
                self.local_messages(event_name, 2),
                has_items(
                    has_entry('value', 'first value'),
                    has_entry('value', 'second value'),
                ),
            )

    def test_extra_headers_required(self):
        event = MockEvent('bound_headers')
        headers = {'must_have': 'this'}

        with self.local_event(event.name, headers=headers):
            self.local_bus.publish(event, headers=headers, payload={'value': 'first'})
            self.local_bus.publish(event, headers=None, payload={'value': 'second'})

            assert_that(
                self.local_messages(event.name, 1),
                has_item(has_entry('value', 'first')),
            )

    def test_publish_wrong_expected_headers_value(self):
        event = MockEvent('wrong_headers_value')
        headers = {'required': True}

        with self.local_event(event.name, headers=headers):
            self.local_bus.publish(
                event, payload={'value': 'something'}, headers={'required': False}
            )

            assert_that(self.local_messages(event.name), is_(empty()))

    def test_publish_ignore_extra_headers(self):
        event = MockEvent('extra_ignored_headers', some='payload')
        headers = {'required': True}

        with self.local_event(event.name, headers=headers):
            self.local_bus.publish(
                event, headers={'required': True, 'other': 1, 'ignored': 'headers'}
            )
            assert_that(
                self.local_messages(event.name, 1),
                has_item(has_entry('some', 'payload')),
            )

    def test_multiple_events(self):
        event1 = MockEvent('event_1', value=1)
        event2 = MockEvent('event_2', value=2)
        event3 = MockEvent('event_3', value=3)
        headers = [{'h': i} for i in range(3)]

        with self.local_event(event1.name, headers=headers[0]):
            with self.local_event(event2.name, headers=headers[1]):
                with self.local_event(event3.name, headers=headers[2]):
                    self.local_bus.publish(event1, headers=headers[0])
                    self.local_bus.publish(event2, headers=headers[1])
                    self.local_bus.publish(event3, headers=headers[2])

                    assert_that(
                        self.local_messages(event1.name, 1),
                        has_item(has_entry('value', 1)),
                    )
                    assert_that(
                        self.local_messages(event2.name, 1),
                        has_item(has_entry('value', 2)),
                    )
                    assert_that(
                        self.local_messages(event3.name, 1),
                        has_item(has_entry('value', 3)),
                    )

    def test_same_event_multiple_headers(self):
        event = MockEvent('test_event', payload='test')
        headers1 = {'test': 1}
        headers2 = {'test': 2}
        headers3 = {'test': 3}
        headers4 = {'test': 4}
        messages = []
        NB_OF_HANDLER_EXECUTIONS = 9  # handlers are per event name (not headers)

        with self.local_event(event.name, headers=headers1):
            with self.local_event(event.name, headers=headers2):
                with self.local_event(event.name, headers=headers3):
                    self.local_bus.publish(event, headers=headers1)
                    self.local_bus.publish(event, headers=headers2)
                    self.local_bus.publish(event, headers=headers3)
                    self.local_bus.publish(event, headers=headers4)
                    messages = self.local_messages(event.name, NB_OF_HANDLER_EXECUTIONS)

        assert_that(messages, has_length(NB_OF_HANDLER_EXECUTIONS))
        for message in messages:
            assert_that(message, has_entry('payload', 'test'))

    def test_publish_queue(self):
        event_name = 'test_queue_publisher'
        event_1 = MockEvent(event_name, value='first payload')
        event_2 = MockEvent(event_name, value='second payload')

        with self.local_event(event_name):
            self.local_bus.publish(event_1)
            self.local_bus.publish_soon(event_2)

            assert_that(
                self.local_messages(event_name, 2),
                has_items(
                    has_entry('value', 'first payload'),
                    has_entry('value', 'second payload'),
                ),
            )

    def test_event_marshaller(self):
        event = MockEvent('marshaller', id=1234, value='something')

        with self.remote_event(event.name):
            self.local_bus.publish(event)

            assert_that(
                self.remote_messages(event.name, 1),
                has_items(
                    has_entry('data', has_entries(id=1234, value='something')),
                    has_entry('name', 'marshaller'),
                    has_entry('origin_uuid', self.local_bus.service_uuid),
                    has_key('timestamp'),
                ),
            )

    def test_event_unmarshaller(self):
        event_name = 'unmarshaller'
        payload = {
            'data': {'name': event_name, 'id': 4567, 'value': 'something'},
            'name': event_name,
            'origin_uuid': '00000000-0000-0000-0000-100000000000',
            'timestamp': datetime.now().isoformat(),
        }

        with self.local_event(event_name):
            self.remote_bus.publish(event_name, payload=payload)

            assert_that(
                self.local_messages(event_name, 1),
                has_items(has_entries(id=4567, value='something')),
            )
