# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    has_entries,
    has_entry,
    is_,
    has_key,
    only_contains,
    calling,
    raises,
)
from xivo_bus.middlewares import EventMarshaller, Middleware, MiddlewareError
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


class TestMiddlewares(BusIntegrationTest):
    asset = 'headers'

    def setUp(self):
        self.event = MockEvent()
        return super().setUp()

    def test_middleware_registration(self):
        assert_that(self.remote_bus.register_middleware('EventLogger'), is_(True))
        assert_that(self.remote_bus.unregister_middleware('EventLogger'), is_(True))

    def test_event_serializer(self):
        service_uuid = '00000000-0000-0000-0000-000000000001'
        headers = {'name': self.event.name}

        with self.local_middleware(EventMarshaller, service_uuid):
            with self.remote_event(self.event.name):
                self.local_bus.publish(self.event, headers=headers)

        assert_that(
            self.remote_messages(self.event.name),
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
        event = 'middleware_deserialization'
        service_uuid = '00000000-0000-0000-0000-000000000002'
        payload = {
            'data': {
                'name': event,
                'id': 4567,
                'value1': 'somevalue',
                'value2': 'someothervalue',
            },
            'name': event,
            'origin_uuid': '00000000-0000-0000-0000-000000000001',
            'timestamp': '------',
        }

        with self.local_middleware(EventMarshaller, service_uuid):
            with self.local_event(event):
                self.remote_bus.publish(event, payload)

        assert_that(
            self.local_messages(event),
            only_contains(
                has_entries(
                    name=event, id=4567, value1='somevalue', value2='someothervalue'
                )
            ),
        )

    def test_bad_middleware(self):
        class BadMiddleware(Middleware):
            def marshal(self, *args):
                pass

            def unmarshal(self, *args):
                pass

        event = 'bad_middleware_event'

        with self.local_middleware(BadMiddleware):
            assert_that(
                calling(self.local_bus.publish).with_args(event, payload="somepayload"),
                raises(MiddlewareError),
            )

    def test_callable_as_middleware(self):
        def do_something(event, headers, payload):
            return headers, 42

        event = 'callable_as_middleware'

        with self.local_middleware(do_something):
            with self.local_event(event):
                self.local_bus.publish(
                    event, headers={'name': event}, payload="payload"
                )

        assert_that(self.local_messages(event), only_contains(42))

    def test_middleware_none(self):
        assert_that(
            calling(self.local_bus.register_middleware).with_args(None),
            raises(TypeError),
        )

    def test_middleware_not_inherited(self):
        class SomeObject(object):
            def marshal(event, headers, payload):
                pass

            def unmarshal(event, headers, payload):
                pass

        assert_that(calling(self.local_middleware(SomeObject)), raises(TypeError))

    def test_middleware_no_required_methods(self):
        class SomeMiddleware(Middleware):
            pass

        assert_that(SomeMiddleware, raises(TypeError))
