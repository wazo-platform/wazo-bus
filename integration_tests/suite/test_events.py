# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    has_entries,
    has_entry,
    has_key,
    only_contains,
)
from .helpers import BusIntegrationTest


class MockEvent:
    name = 'test_event'
    routing_key = 'test.routing.key'

    def __init__(self):
        self.id = 1234
        self.value1 = 'payload1'
        self.value2 = 'payload2'

    def marshal(self):
        return dict(id=self.id, value1=self.value1, value2=self.value2)


class TestEvents(BusIntegrationTest):
    asset = 'headers'
    TEST_WAZO_EVENTS = True

    def setUp(self):
        return super().setUp()

    def test_wazo_event_marshaller(self):
        event = MockEvent()
        headers = {'name': event.name}

        with self.remote_event(event.name):
            self.local_bus.publish(event, headers=headers)

        assert_that(
            self.remote_messages(event.name),
            only_contains(
                has_entry(
                    'data',
                    has_entries(
                        name='test_event', id=1234, value1='payload1', value2='payload2'
                    ),
                ),
                has_entry('name', 'test_event'),
                has_entry('origin_uuid', self.local_bus.service_uuid),
                has_key('timestamp'),
            ),
        )

    def test_wazo_event_unmarshaller(self):
        event = 'test_event_unmarshal'
        payload = {
            'data': {
                'name': event,
                'id': 4567,
                'value1': 'somevalue',
                'value2': 'someothervalue',
            },
            'name': event,
            'origin_uuid': '00000000-0000-0000-0000-100000000000',
            'timestamp': '------',
        }

        with self.local_event(event):
            self.remote_bus.publish(event, payload=payload)

        assert_that(
            self.local_messages(event),
            only_contains(
                has_entries(
                    name=event, id=4567, value1='somevalue', value2='someothervalue'
                )
            ),
        )
