# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime
from hamcrest import (
    assert_that,
    has_item,
    is_,
    empty,
    has_entry,
    has_items,
    has_entries,
    has_key,
)

from .helpers.base import BusIntegrationTest
from .helpers.events import MockEvent


class TestRoutingKey(BusIntegrationTest):
    asset = 'topic'

    def test_bind_unbind(self):
        event = MockEvent(
            'bind_unbind', routing_key='events.bus.bind_unbind', data='payload'
        )

        with self.local_event(event.name, routing_key=event.routing_key):
            self.local_bus.publish(event)
        self.local_bus.publish(event)

        assert_that(
            self.local_messages(event.name), has_item(has_entry('data', 'payload'))
        )

    def test_good_routing_key(self):
        event = MockEvent('good_routing_key', data='payload')

        with self.local_event(event.name, routing_key='events.bus.good.#'):
            self.local_bus.publish(event, routing_key='events.bus.good.1.ok')

        assert_that(
            self.local_messages(event.name), has_item(has_entry('data', 'payload'))
        )

    def test_wrong_routing_key(self):
        event = MockEvent('wrong_routing_key', data='something')

        with self.local_event(event.name, routing_key='events.bus.good.#'):
            self.local_bus.publish(event, routing_key='events.bus.wrong')

        assert_that(self.local_messages(event.name), is_(empty()))

    def test_no_event_routing_key(self):
        event = MockEvent('no_key', data='something')

        with self.local_event(event.name, routing_key=None):
            self.local_bus.publish(event, routing_key='events.bus.somewhere')

        assert_that(self.local_messages(event.name), is_(empty()))

    def test_no_routing_key(self):
        event = MockEvent('no_publish_key', data='payload')

        with self.local_event(event.name, routing_key='events.bus.good.#'):
            self.local_bus.publish(event, routing_key=None)

        assert_that(self.local_messages(event.name), is_(empty()))

    def test_headers_disabled_when_using_routing_key(self):
        event = MockEvent('headers_test', data='payload')

        with self.local_event(
            event.name, headers={'required': True}, routing_key='events.#'
        ):
            self.local_bus.publish(
                event, headers={'required': False}, routing_key='events.1'
            )

        assert_that(
            self.local_messages(event.name), has_item(has_entry('data', 'payload'))
        )

    def test_message_marshalling(self):
        event = MockEvent(
            'marshaller', id=1234, value='something', routing_key='some.key.1'
        )

        with self.remote_event(event.name, routing_key='some.key.#'):
            self.local_bus.publish(event)

        assert_that(
            self.remote_messages(event.name),
            has_items(
                has_entry('data', has_entries(id=1234, value='something')),
                has_entry('name', 'marshaller'),
                has_entry('origin_uuid', self.local_bus.service_uuid),
                has_key('timestamp'),
            ),
        )

    def test_message_unmarshalling(self):
        event_name = 'unmarshaller'
        payload = {
            'data': {'name': event_name, 'id': 4567, 'value': 'something'},
            'name': event_name,
            'origin_uuid': '00000000-0000-0000-0000-100000000000',
            'timestamp': datetime.now().isoformat(),
        }

        with self.local_event(event_name, routing_key='other.key.#'):
            self.remote_bus.publish(
                event_name, payload=payload, routing_key='other.key.1'
            )

        assert_that(
            self.local_messages(event_name),
            has_items(has_entries(id=4567, value='something')),
        )
