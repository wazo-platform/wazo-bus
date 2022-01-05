# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_entries, has_entry, is_, has_key, only_contains
from .helpers import BusIntegrationTest


class MockEvent:
    name = 'test_event'
    routing_key = 'test.routing.key'

    def __init__(self):
        self.id = 1234
        self.value1 = 'payload1'
        self.value2 = 'payload2'


class TestMiddlewares(BusIntegrationTest):
    asset = 'headers'

    def setUp(self):
        self.event = MockEvent()
        return super().setUp()

    def test_binding(self):
        assert_that(self.bus.add_middleware('consumer', 'EchoMiddleware'), is_(True))
        assert_that(self.bus.remove_middleware('consumer', 'EchoMiddleware'), is_(True))

    def test_event_serializer(self):
        service_uuid = '00000000-0000-0000-0000-000000000001'

        with self.use_middleware('publisher', 'EventProcessor', service_uuid):
            with self.use_event(self.event.name):
                self.bus.publish_event(self.event)

        assert_that(
            self.bus.get_messages(self.event.name),
            only_contains(
                has_entry(
                    'data',
                    has_entries(
                        name='test_event', id=1234, value1='payload1', value2='payload2'
                    ),
                ),
                has_entry('name', 'test_event'),
                has_entry('origin_uuid', service_uuid),
                has_key('timestamp'),
            ),
        )

    def test_event_deserializer(self):
        service_uuid = '00000000-0000-0000-0000-000000000002'
        payload = {
            'data': {
                'name': self.event.name,
                'id': self.event.id,
                'value1': self.event.value1,
                'value2': self.event.value2,
            },
            'name': self.event.name,
            'origin_uuid': service_uuid,
            'timestamp': '------',
        }

        with self.use_middleware('consumer', 'EventProcessor', service_uuid):
            with self.use_event(self.event.name):
                self.bus.publish(self.event.name, payload)

        messages = self.bus.get_messages(self.event.name)
        assert_that(
            messages,
            only_contains(
                has_entries(
                    name=self.event.name,
                    id=self.event.id,
                    value1=self.event.value1,
                    value2=self.event.value2,
                )
            ),
        )
