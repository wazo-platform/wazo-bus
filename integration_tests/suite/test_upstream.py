# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from uuid import uuid4

from hamcrest import assert_that, empty, equal_to, has_entry, has_item, has_length, is_
from kombu import Connection, Exchange
from kombu.exceptions import OperationalError
from wazo_test_helpers import until

from wazo_bus.consumer import BusConsumer
from wazo_bus.publisher import BusPublisher

from .helpers.accumulator import MessageAccumulator
from .helpers.base import BusIntegrationTest
from .helpers.events import MockEvent

DOWNSTREAM_EXCHANGE_NAME = 'bus-integration-tests-downstream'
MISSING_UPSTREAM_EXCHANGE_NAME = 'bus-integration-tests-missing-upstream'


class TestUpstream(BusIntegrationTest):
    asset = 'headers'

    def setUp(self):
        super().setUp()
        self.messages = MessageAccumulator()
        self.consumer = self.make_consumer(self.EXCHANGE_NAME)

    def tearDown(self):
        self.consumer.stop()
        super().tearDown()

    def make_consumer(self, upstream_exchange_name):
        consumer = BusConsumer(
            name='upstream-consumer',
            service_uuid=str(uuid4()),
            host='127.0.0.1',
            port=self.service_port(5672, 'rabbitmq'),
            exchange_name=DOWNSTREAM_EXCHANGE_NAME,
            exchange_type='headers',
            upstream_exchange_name=upstream_exchange_name,
        )
        consumer.start()
        return consumer

    def subscribe(self, event_name, headers=None):
        handler = self.messages.create_handler(event_name)
        self.consumer.subscribe(event_name, handler, headers)
        return handler

    def received(self, event_name, expected, timeout=3.0):
        def test():
            return self.messages.count(event_name) == expected

        try:
            until.true(test, timeout=timeout, interval=0.1)
        except until.NoMoreTries:
            pass
        return self.messages.pop(event_name)

    def upstream_bindings(self, upstream_exchange_name, event_name):
        output = self.docker_exec(
            [
                'rabbitmqctl',
                '--silent',
                'list_bindings',
                'source_name',
                'destination_name',
                'arguments',
            ],
            'rabbitmq',
        ).decode()
        return [
            line
            for line in output.splitlines()
            if line.startswith(
                f'{upstream_exchange_name}\t{DOWNSTREAM_EXCHANGE_NAME}\t'
            )
            and event_name in line
        ]

    def test_event_from_upstream_exchange(self):
        event = MockEvent('upstream_event', value='from upstream')
        self.subscribe(event.name)
        assert_that(self.consumer.wait_synchronized(), is_(True))

        self.local_bus.publish(event)

        assert_that(
            self.received(event.name, 1),
            has_item(has_entry('value', 'from upstream')),
        )

    def test_upstream_binding_goes_with_last_handler(self):
        shared_event = 'upstream_shared_event'
        # NOTE: keeps the auto-delete downstream exchange alive when the shared
        # event goes
        self.subscribe('upstream_keeper_event')
        # NOTE: different headers, else both handlers share one queue binding
        handler1 = self.subscribe(shared_event, headers={'handler': 1})
        handler2 = self.subscribe(shared_event, headers={'handler': 2})
        assert_that(self.consumer.wait_synchronized(), is_(True))
        assert_that(
            self.upstream_bindings(self.EXCHANGE_NAME, shared_event), has_length(1)
        )

        assert_that(self.consumer.unsubscribe(shared_event, handler1), is_(True))
        assert_that(self.consumer.wait_synchronized(), is_(True))
        assert_that(
            self.upstream_bindings(self.EXCHANGE_NAME, shared_event), has_length(1)
        )

        assert_that(self.consumer.unsubscribe(shared_event, handler2), is_(True))
        assert_that(self.consumer.wait_synchronized(), is_(True))
        assert_that(
            self.upstream_bindings(self.EXCHANGE_NAME, shared_event), is_(empty())
        )
        assert_that(
            self.upstream_bindings(self.EXCHANGE_NAME, 'upstream_keeper_event'),
            has_length(1),
        )

    def test_resubscribe_after_every_event_is_gone(self):
        # NOTE: the last unbinding deletes the auto-delete downstream exchange
        event = MockEvent('resubscribed_upstream_event', value='again')
        handler = self.subscribe(event.name)
        assert_that(self.consumer.wait_synchronized(), is_(True))
        queue_name = self.consumer._ConsumerMixin__queue.name
        assert_that(self.consumer.unsubscribe(event.name, handler), is_(True))
        assert_that(self.consumer.wait_synchronized(), is_(True))

        self.subscribe(event.name)
        assert_that(self.consumer.wait_synchronized(), is_(True))
        self.local_bus.publish(event)

        assert_that(self.received(event.name, 1), has_item(has_entry('value', 'again')))
        # healed without a reconnection, which would have made a new queue
        assert_that(self.consumer._ConsumerMixin__queue.name, equal_to(queue_name))

    def test_upstream_exchange_missing_at_subscribe(self):
        self.consumer.stop()
        self.consumer = self.make_consumer(MISSING_UPSTREAM_EXCHANGE_NAME)
        queue_name = self.consumer._ConsumerMixin__queue.name
        event = MockEvent('late_upstream_event', value='late')

        self.subscribe(event.name)

        assert_that(self.consumer.wait_synchronized(timeout=1.0), is_(False))

        url = f'amqp://guest:guest@127.0.0.1:{self.service_port(5672, "rabbitmq")}//'
        upstream = Exchange(MISSING_UPSTREAM_EXCHANGE_NAME, 'headers', durable=True)
        with Connection(url) as connection:
            upstream(connection.default_channel).declare()
        try:
            assert_that(self.consumer.wait_synchronized(), is_(True))

            publisher = BusPublisher(
                service_uuid=str(uuid4()),
                host='127.0.0.1',
                port=self.service_port(5672, 'rabbitmq'),
                exchange_name=MISSING_UPSTREAM_EXCHANGE_NAME,
                exchange_type='headers',
            )
            publisher.publish(event)

            assert_that(
                self.received(event.name, 1),
                has_item(has_entry('value', 'late')),
            )
            # retried in place, not through a reconnection
            assert_that(self.consumer._ConsumerMixin__queue.name, equal_to(queue_name))
        finally:
            with Connection(url) as connection:
                upstream(connection.default_channel).delete()

    def test_upstream_binding_restored_after_rabbitmq_restart(self):
        event = MockEvent('restored_upstream_event', value='after restart')
        self.subscribe(event.name)
        assert_that(self.consumer.wait_synchronized(), is_(True))

        self.stop_rabbitmq()
        self.start_rabbitmq()
        self.consumer._connection_params = self.local_bus._connection_params
        self.consumer.connection.switch(self.local_bus.url)

        def event_received():
            try:
                self.local_bus.publish(event)
            except OperationalError:
                return []
            return self.received(event.name, 1, timeout=1.0)

        messages = until.true(event_received, timeout=30, interval=0.5)

        assert_that(messages, has_item(has_entry('value', 'after restart')))
        assert_that(
            self.upstream_bindings(self.EXCHANGE_NAME, event.name), has_length(1)
        )
