# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_entries, is_, has_key, has_items, has_item

from .helpers import BusIntegrationTest


class TestMiddlewares(BusIntegrationTest):
    asset = 'headers'

    def test_add_remove(self):
        assert_that(
            self.bus.add_middlewares('consumer', 'EchoMiddleware', 'Test'), is_(True)
        )
        assert_that(self.bus.remove_middleware('consumer', 'EchoMiddleware'), is_(True))

    def test_middleware_event_publisher(self):
        class MockEvent(object):
            name = 'test_publisher_middleware'
            some_dict = {'key1': 'value1', 'key2': 'value2'}

        event = MockEvent()
        service_uuid = '00000000-0000-0000-0000-000000000001'

        with self.use_middleware(
            'publisher', 'EventPublisherMiddleware', service_uuid=service_uuid
        ):
            with self.use_event(event.name):
                self.bus.publish_event_object(MockEvent())

        assert_that(
            self.bus.get_messages(event.name),
            has_items(
                has_entries(
                    data=has_entries(name=event.name, some_dict=event.some_dict),
                    name=event.name,
                    origin_uuid=service_uuid,
                ),
                has_key('timestamp'),
            ),
        )

    def test_middleware_event_consumer(self):
        event = 'event_test_consumer_middleware'
        service_uuid = '00000000-0000-0000-0000-000000000002'

        published_event = {
            'data': {'name': event, 'something': 'somevalue'},
            'name': event,
            'origin_uuid': service_uuid,
        }

        with self.use_middleware('consumer', 'EventConsumerMiddleware'):
            with self.use_event(event):
                self.bus.publish(event, published_event)

        assert_that(
            self.bus.get_messages(event),
            has_item(has_entries(name=event, something='somevalue')),
        )
