# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from threading import Thread
from time import monotonic
from unittest import TestCase
from unittest.mock import Mock, patch

from amqp.exceptions import AccessRefused, NotFound
from amqp.serialization import dumps, loads
from hamcrest import (
    assert_that,
    empty,
    equal_to,
    has_item,
    has_length,
    is_not,
    less_than,
    same_instance,
    starts_with,
)
from kombu import Exchange
from kombu import binding as Binding
from kombu.transport import pyamqp

from ..consumer import BusConsumer
from ..mixins import broker_tells_numbers_apart


class TestUpstreamBindings(TestCase):
    def setUp(self):
        self.consumer = BusConsumer(
            name='upstream-unit',
            exchange_name='downstream',
            exchange_type='headers',
            upstream_exchange_name='upstream',
        )
        self.consumer.connection = Mock(
            connection_errors=(), channel_errors=(NotFound,)
        )
        self.handler = Mock()
        self.consumer.subscribe('some_event', self.handler)
        self.consumer.get_consumers(Mock(), Mock())

    def tick(self, upstream_error):
        def bind(entity, channel=None):
            if isinstance(entity, Exchange):
                raise upstream_error

        with patch.object(Binding, 'bind', side_effect=bind):
            with self.assertLogs('BusConsumer', level=logging.DEBUG) as logs:
                self.consumer.on_iteration()
        self.messages = [r.getMessage() for r in logs.records]
        return [r.levelno for r in logs.records if 'will retry' in r.getMessage()]

    def test_the_warning_names_the_upstream_exchange(self):
        self.tick(NotFound('no exchange'))

        assert_that(
            self.messages,
            has_item(
                starts_with(
                    'Failed to update bindings from upstream exchange \'upstream\' to \'downstream\''
                )
            ),
        )

    def test_an_unbind_not_found_counts_every_removal_as_done(self):
        other_handler = Mock()
        self.consumer.subscribe('other_event', other_handler)
        with patch.object(Binding, 'bind'):
            self.consumer.on_iteration()
        self.consumer.unsubscribe('some_event', self.handler)
        self.consumer.unsubscribe('other_event', other_handler)
        self.consumer.subscribe('new_event', Mock())
        self.consumer.connection.channel.side_effect = lambda: Mock()
        calls = []

        def unbind(entity, channel=None):
            if isinstance(entity, Exchange):
                calls.append(('unbind', channel))
                if len(calls) == 1:
                    raise NotFound('no exchange \'upstream\'')

        def bind(entity, channel=None):
            if isinstance(entity, Exchange):
                calls.append(('bind', channel))

        with patch.object(Binding, 'unbind', side_effect=unbind):
            with patch.object(Binding, 'bind', side_effect=bind):
                self.consumer.on_iteration()

        assert_that([name for name, _ in calls], equal_to(['unbind', 'bind']))
        failed_channel = calls[0][1]
        assert_that(calls[1][1], is_not(same_instance(failed_channel)))
        assert_that(failed_channel.exchange_declare.called, equal_to(False))
        assert_that(self.consumer.wait_synchronized(timeout=0), equal_to(True))

    def test_a_repeated_error_warns_once_then_again_after_a_success(self):
        missing = NotFound('no exchange \'upstream\'')

        assert_that(self.tick(missing), equal_to([logging.WARNING]))
        assert_that(self.tick(missing), equal_to([logging.DEBUG]))
        assert_that(self.consumer.wait_synchronized(timeout=0), equal_to(False))

        with patch.object(Binding, 'bind'):
            self.consumer.on_iteration()
        assert_that(self.consumer.wait_synchronized(timeout=0), equal_to(True))

        self.consumer.unsubscribe('some_event', self.handler)
        self.consumer.subscribe('other_event', Mock())
        assert_that(self.tick(missing), equal_to([logging.WARNING]))

    def test_a_distinct_error_warns_again(self):
        assert_that(self.tick(NotFound('first')), equal_to([logging.WARNING]))
        assert_that(self.tick(NotFound('second')), equal_to([logging.WARNING]))

    def test_an_upstream_change_alone_wakes_a_waiter(self):
        result = {}

        def wait():
            started = monotonic()
            result['synced'] = self.consumer.wait_synchronized(timeout=5.0)
            result['elapsed'] = monotonic() - started

        waiter = Thread(target=wait)
        waiter.start()
        with patch.object(Binding, 'bind'):
            self.consumer.on_iteration()
        waiter.join()

        assert_that(result['synced'], equal_to(True))
        assert_that(result['elapsed'], less_than(1.0))

    def test_a_resubscribe_during_a_batch_ends_bound_on_the_next_tick(self):
        calls = []

        def bind_and_resubscribe(entity, channel=None):
            if not isinstance(entity, Exchange):
                return
            calls.append('bind')
            if len(calls) == 1:
                self.consumer.unsubscribe('some_event', self.handler)
                self.consumer.subscribe('some_event', self.handler)

        def unbind(entity, channel=None):
            if isinstance(entity, Exchange):
                calls.append('unbind')

        with patch.object(Binding, 'bind', side_effect=bind_and_resubscribe):
            with patch.object(Binding, 'unbind', side_effect=unbind):
                self.consumer.on_iteration()
                assert_that(self.consumer.wait_synchronized(timeout=0), equal_to(False))
                self.consumer.on_iteration()

        assert_that(calls, equal_to(['bind', 'unbind', 'bind']))
        assert_that(self.consumer.wait_synchronized(timeout=0), equal_to(True))

    def test_a_queue_binding_waits_for_its_upstream_binding(self):
        bound = []

        def bind_failing_upstream(entity, channel=None):
            if isinstance(entity, Exchange):
                raise NotFound('no exchange')
            bound.append(entity)

        def bind(entity, channel=None):
            bound.append(entity)

        with patch.object(Binding, 'bind', side_effect=bind_failing_upstream):
            self.consumer.on_iteration()
        assert_that(bound, empty())
        assert_that(self.consumer.wait_synchronized(timeout=0), equal_to(False))

        with patch.object(Binding, 'bind', side_effect=bind):
            self.consumer.on_iteration()
        upstream_first = [isinstance(entity, Exchange) for entity in bound]
        assert_that(upstream_first, equal_to([True, False]))
        assert_that(self.consumer.wait_synchronized(timeout=0), equal_to(True))

    def test_a_reconnection_declares_the_queue_without_bindings(self):
        with patch.object(Binding, 'bind'):
            self.consumer.on_iteration()

        self.consumer.get_consumers(Mock(), Mock())

        assert_that(self.consumer._ConsumerMixin__queue.bindings, empty())

    def test_a_binding_never_attempted_is_not_failing(self):
        assert_that(self.consumer.consumer_bindings_failing(), equal_to(False))

    def test_a_failed_upstream_binding_is_failing_until_bound(self):
        self.tick(NotFound('no exchange'))
        assert_that(self.consumer.consumer_bindings_failing(), equal_to(True))

        with patch.object(Binding, 'bind'):
            self.consumer.on_iteration()
        assert_that(self.consumer.consumer_bindings_failing(), equal_to(False))

    def test_a_failed_upstream_binding_no_longer_wanted_is_not_failing(self):
        self.tick(NotFound('no exchange'))

        self.consumer.unsubscribe('some_event', self.handler)

        assert_that(self.consumer.consumer_bindings_failing(), equal_to(False))

    def test_a_failed_queue_binding_is_failing_until_bound(self):
        self.consumer.connection.channel_errors = (NotFound, AccessRefused)

        def bind_failing_queue(entity, channel=None):
            if not isinstance(entity, Exchange):
                raise AccessRefused('refused')

        with patch.object(Binding, 'bind', side_effect=bind_failing_queue):
            self.consumer.on_iteration()
        assert_that(self.consumer.consumer_bindings_failing(), equal_to(True))

        with patch.object(Binding, 'bind'):
            self.consumer.on_iteration()
        assert_that(self.consumer.consumer_bindings_failing(), equal_to(False))


class TestUpstreamExchange(TestCase):
    def make_consumer(self, **kwargs):
        return BusConsumer(
            name='upstream-unit',
            exchange_name='downstream',
            exchange_type='headers',
            **kwargs,
        )

    def declared(self, consumer):
        channel = Mock()
        consumer.get_consumers(Mock(), channel)
        kwargs = channel.exchange_declare.call_args.kwargs
        return {'auto_delete': kwargs['auto_delete'], 'durable': kwargs['durable']}

    def test_the_consuming_exchange_is_transient_auto_delete_with_an_upstream(self):
        consumer = self.make_consumer(
            upstream_exchange_name='upstream',
            exchange_durable=True,
            exchange_kwargs={'auto_delete': False},
        )

        assert_that(
            self.declared(consumer),
            equal_to({'auto_delete': True, 'durable': False}),
        )

    def test_the_consuming_exchange_is_unchanged_without_an_upstream(self):
        consumer = self.make_consumer()

        assert_that(
            self.declared(consumer),
            equal_to({'auto_delete': False, 'durable': True}),
        )

    def test_the_queue_is_declared_with_its_bindings_without_an_upstream(self):
        consumer = self.make_consumer()
        consumer.subscribe('some_event', Mock())

        consumer.get_consumers(Mock(), Mock())

        assert_that(consumer._ConsumerMixin__queue.bindings, has_length(1))


TENANT_1 = '00000000-0000-4000-8000-000000000001'
TENANT_2 = '00000000-0000-4000-8000-000000000002'
MOBILE_EVENTS = (
    'chatd_user_room_message_created',
    'call_push_notification',
    'call_cancel_push_notification',
    'user_voicemail_message_created',
    'global_voicemail_message_created',
    'missed_call',
)


def make_headers_consumer(**kwargs):
    return BusConsumer(
        name='bind-keys-unit',
        exchange_name='downstream',
        exchange_type='headers',
        **kwargs,
    )


def subscriber_headers(number, tenant_uuid=None):
    headers = {
        'x-subscription': f'subscription-{number}',
        f'user_uuid:user-{number}': True,
        'origin_uuid': 'wazo-uuid',
    }
    if tenant_uuid:
        headers['tenant_uuid'] = tenant_uuid
    return headers


def queue_bindings(consumer):
    consumer.get_consumers(Mock(), Mock())
    return sorted(
        (binding.routing_key or '', sorted(binding.arguments.items()))
        for binding in consumer._ConsumerMixin__queue.bindings
    )


def reduced(name, tenant_uuid=None, routing_key=''):
    arguments = {'name': name, 'x-match': 'all'}
    if tenant_uuid:
        arguments['tenant_uuid'] = tenant_uuid
    return (routing_key, sorted(arguments.items()))


def deliver(consumer, headers, data=None):
    message = Mock(headers=dict(headers), payload={'data': data or {}})
    consumer._ConsumerMixin__on_message_received(None, message)


class TestWithoutBindKeys(TestCase):
    def test_each_subscription_keeps_its_own_queue_binding(self):
        consumer = make_headers_consumer()
        consumer.subscribe('some_event', Mock(), headers=subscriber_headers(1))
        consumer.subscribe('some_event', Mock(), headers=subscriber_headers(2))

        bindings = queue_bindings(consumer)

        assert_that(bindings, has_length(2))
        assert_that(
            bindings,
            has_item(
                (
                    '',
                    sorted(
                        {
                            **subscriber_headers(1),
                            'name': 'some_event',
                            'x-match': 'all',
                        }.items()
                    ),
                )
            ),
        )

    def test_every_handler_of_the_event_is_called_whatever_the_headers(self):
        consumer = make_headers_consumer()
        first, second = Mock(), Mock()
        consumer.subscribe('some_event', first, headers=subscriber_headers(1))
        consumer.subscribe('some_event', second, headers=subscriber_headers(2))

        deliver(consumer, {'name': 'some_event', 'user_uuid:user-1': True})

        assert_that(first.call_count, equal_to(1))
        assert_that(second.call_count, equal_to(1))


class TestBindKeysBindings(TestCase):
    def test_one_tenant_binds_once_per_event_name(self):
        consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
        for number in range(3572):
            headers = subscriber_headers(number, TENANT_1)
            for event in MOBILE_EVENTS:
                consumer.subscribe(event, Mock(), headers=headers)

        assert_that(
            queue_bindings(consumer),
            equal_to(sorted(reduced(event, TENANT_1) for event in MOBILE_EVENTS)),
        )

    def test_two_tenants_bind_once_per_event_name_and_tenant(self):
        consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
        for number in range(3572):
            headers = subscriber_headers(number, (TENANT_1, TENANT_2)[number % 2])
            for event in MOBILE_EVENTS:
                consumer.subscribe(event, Mock(), headers=headers)

        assert_that(
            queue_bindings(consumer),
            equal_to(
                sorted(
                    reduced(event, tenant)
                    for event in MOBILE_EVENTS
                    for tenant in (TENANT_1, TENANT_2)
                )
            ),
        )

    def test_a_master_tenant_subscription_binds_by_name_alone(self):
        consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
        consumer.subscribe('some_event', Mock(), headers=subscriber_headers(1))

        assert_that(queue_bindings(consumer), equal_to([reduced('some_event')]))

    def test_no_bind_keys_binds_once_per_name_whatever_the_tenants(self):
        consumer = make_headers_consumer(bind_keys=())
        consumer.subscribe(
            'some_event', Mock(), headers=subscriber_headers(1, TENANT_1)
        )
        consumer.subscribe(
            'some_event', Mock(), headers=subscriber_headers(2, TENANT_2)
        )
        consumer.subscribe('some_event', Mock(), headers=subscriber_headers(3))

        assert_that(queue_bindings(consumer), equal_to([reduced('some_event')]))

    def test_a_match_any_subscription_binds_by_name_alone(self):
        consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
        consumer.subscribe(
            'some_event',
            Mock(),
            headers=subscriber_headers(1, TENANT_1),
            headers_match_all=False,
        )

        assert_that(queue_bindings(consumer), equal_to([reduced('some_event')]))

    def test_each_subscription_keeps_its_full_binding(self):
        consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
        handler = Mock()
        consumer.subscribe(
            'some_event', handler, headers=subscriber_headers(1, TENANT_1)
        )

        [subscription] = consumer._ConsumerMixin__subscriptions['some_event']

        assert_that(subscription.handler, same_instance(handler))
        assert_that(
            subscription.binding.arguments,
            equal_to(
                {
                    **subscriber_headers(1, TENANT_1),
                    'name': 'some_event',
                    'x-match': 'all',
                }
            ),
        )

    def test_a_consumer_without_bind_keys_takes_any_exchange_type(self):
        for exchange_type in ('topic', 'direct', 'fanout', 'headers', ''):
            BusConsumer(
                name='bind-keys-unit',
                exchange_name='downstream',
                exchange_type=exchange_type,
            )

    def test_bind_keys_reject_an_x_match_other_than_all_or_any(self):
        for x_match in ('all-with-x', 'any-with-x', 'none'):
            consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
            with self.assertRaises(ValueError):
                consumer.subscribe(
                    'some_event',
                    Mock(),
                    headers={**subscriber_headers(1, TENANT_1), 'x-match': x_match},
                )
            assert_that(consumer._ConsumerMixin__subscriptions, equal_to({}))
            assert_that(queue_bindings(consumer), equal_to([]))

    def test_without_bind_keys_any_x_match_is_kept(self):
        consumer = make_headers_consumer()
        consumer.subscribe(
            'some_event',
            Mock(),
            headers={**subscriber_headers(1), 'x-match': 'all-with-x'},
        )

        [binding] = queue_bindings(consumer)
        assert_that(dict(binding[1])['x-match'], equal_to('all-with-x'))

    def test_bind_keys_on_a_non_headers_exchange_raises(self):
        for exchange_type in ('topic', 'direct', 'fanout', ''):
            with self.assertRaises(ValueError):
                BusConsumer(
                    name='bind-keys-unit',
                    exchange_name='downstream',
                    exchange_type=exchange_type,
                    bind_keys=('tenant_uuid',),
                )


class TestBindKeysUnsubscribe(TestCase):
    def setUp(self):
        self.consumer = make_headers_consumer(bind_keys=('tenant_uuid',))

    def subscribe(self, number, tenant_uuid, event='some_event', routing_key=None):
        handler = Mock()
        self.consumer.subscribe(
            event,
            handler,
            headers=subscriber_headers(number, tenant_uuid),
            routing_key=routing_key,
        )
        return handler

    def test_the_reduced_binding_stays_until_the_last_subscription(self):
        handlers = [self.subscribe(number, TENANT_1) for number in range(3)]
        other_tenant = self.subscribe(9, TENANT_2)

        for handler in handlers[:-1]:
            assert_that(
                self.consumer.unsubscribe('some_event', handler), equal_to(True)
            )
        assert_that(
            queue_bindings(self.consumer),
            equal_to(
                sorted(
                    [reduced('some_event', TENANT_1), reduced('some_event', TENANT_2)]
                )
            ),
        )

        self.consumer.unsubscribe('some_event', handlers[-1])
        assert_that(
            queue_bindings(self.consumer),
            equal_to([reduced('some_event', TENANT_2)]),
        )

        self.consumer.unsubscribe('some_event', other_tenant)
        assert_that(queue_bindings(self.consumer), empty())

    def test_two_subscriptions_with_identical_headers_share_one_binding(self):
        first = Mock()
        second = Mock()
        headers = subscriber_headers(1, TENANT_1)
        self.consumer.subscribe('some_event', first, headers=headers)
        self.consumer.subscribe('some_event', second, headers=headers)

        self.consumer.unsubscribe('some_event', first)
        assert_that(
            queue_bindings(self.consumer), equal_to([reduced('some_event', TENANT_1)])
        )

        self.consumer.unsubscribe('some_event', second)
        assert_that(queue_bindings(self.consumer), empty())

    def test_an_unknown_handler_changes_nothing(self):
        self.subscribe(1, TENANT_1)

        assert_that(self.consumer.unsubscribe('some_event', Mock()), equal_to(False))
        assert_that(
            queue_bindings(self.consumer), equal_to([reduced('some_event', TENANT_1)])
        )

    def test_each_routing_key_keeps_its_binding_until_its_own_last_subscription(self):
        first = self.subscribe(1, TENANT_1, routing_key='one')
        second = self.subscribe(2, TENANT_1, routing_key='two')
        third = self.subscribe(3, TENANT_1, routing_key='two')

        self.consumer.unsubscribe('some_event', second)
        assert_that(
            queue_bindings(self.consumer),
            equal_to(
                sorted(
                    [
                        reduced('some_event', TENANT_1, 'one'),
                        reduced('some_event', TENANT_1, 'two'),
                    ]
                )
            ),
        )

        self.consumer.unsubscribe('some_event', first)
        assert_that(
            queue_bindings(self.consumer),
            equal_to([reduced('some_event', TENANT_1, 'two')]),
        )

        self.consumer.unsubscribe('some_event', third)
        assert_that(queue_bindings(self.consumer), empty())

    def test_subscribe_then_unsubscribe_keeps_the_binding(self):
        previous = self.subscribe(1, TENANT_1)

        self.consumer.subscribe(
            'some_event', Mock(), headers=subscriber_headers(2, TENANT_1)
        )
        self.consumer.unsubscribe('some_event', previous)

        assert_that(
            queue_bindings(self.consumer), equal_to([reduced('some_event', TENANT_1)])
        )

    def test_unsubscribe_then_subscribe_ends_with_the_binding(self):
        previous = self.subscribe(1, TENANT_1)

        self.consumer.unsubscribe('some_event', previous)
        assert_that(queue_bindings(self.consumer), empty())
        self.subscribe(1, TENANT_1)

        assert_that(
            queue_bindings(self.consumer), equal_to([reduced('some_event', TENANT_1)])
        )

    def test_a_shared_binding_is_unbound_from_the_broker_after_the_last_one(self):
        self.consumer.connection = Mock(connection_errors=(), channel_errors=())
        first = self.subscribe(1, TENANT_1)
        second = self.subscribe(2, TENANT_1)
        self.consumer.get_consumers(Mock(), Mock())

        with patch.object(Binding, 'unbind', autospec=True) as unbind_mock:
            self.consumer.unsubscribe('some_event', first)
            self.consumer.on_iteration()
            assert_that(unbind_mock.call_count, equal_to(0))

            self.consumer.unsubscribe('some_event', second)
            self.consumer.on_iteration()
            assert_that(unbind_mock.call_count, equal_to(1))
            binding = unbind_mock.call_args.args[0]
            assert_that(
                binding.arguments,
                equal_to(
                    {'name': 'some_event', 'tenant_uuid': TENANT_1, 'x-match': 'all'}
                ),
            )
        assert_that(self.consumer.wait_synchronized(timeout=0), equal_to(True))

    def test_unsubscribe_then_subscribe_between_ticks_touches_no_broker_binding(self):
        self.consumer.connection = Mock(connection_errors=(), channel_errors=())
        previous = self.subscribe(1, TENANT_1)
        self.consumer.get_consumers(Mock(), Mock())

        with patch.object(Binding, 'bind') as bind, patch.object(
            Binding, 'unbind'
        ) as unbind:
            self.consumer.unsubscribe('some_event', previous)
            self.subscribe(1, TENANT_1)
            self.consumer.on_iteration()

            assert_that(bind.call_count, equal_to(0))
            assert_that(unbind.call_count, equal_to(0))
        assert_that(self.consumer.wait_synchronized(timeout=0), equal_to(True))


class TestBindKeysDispatch(TestCase):
    def setUp(self):
        self.consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
        self.user_a = Mock()
        self.user_b = Mock()
        self.consumer.subscribe(
            'some_event', self.user_a, headers=subscriber_headers('a', TENANT_1)
        )
        self.consumer.subscribe(
            'some_event', self.user_b, headers=subscriber_headers('b', TENANT_1)
        )

    def test_only_the_handler_whose_headers_match_is_called(self):
        deliver(
            self.consumer,
            {
                'name': 'some_event',
                'tenant_uuid': TENANT_1,
                'origin_uuid': 'wazo-uuid',
                'user_uuid:user-a': True,
            },
            {'for': 'a'},
        )

        self.user_a.assert_called_once_with({'for': 'a'})
        self.user_b.assert_not_called()

    def test_a_header_with_another_value_does_not_match(self):
        deliver(
            self.consumer,
            {
                'name': 'some_event',
                'tenant_uuid': TENANT_2,
                'origin_uuid': 'wazo-uuid',
                'user_uuid:user-a': True,
            },
        )

        self.user_a.assert_not_called()
        self.user_b.assert_not_called()

    def test_the_subscription_x_keys_are_not_required_in_the_message(self):
        consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
        handler = Mock()
        consumer.subscribe(
            'some_event',
            handler,
            headers={'x-subscription': 'one', 'tenant_uuid': TENANT_1},
        )

        deliver(consumer, {'name': 'some_event', 'tenant_uuid': TENANT_1})

        assert_that(handler.call_count, equal_to(1))

    def test_a_match_any_subscription_receives_every_message_of_its_name(self):
        consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
        handler = Mock()
        consumer.subscribe(
            'some_event',
            handler,
            headers={'user_uuid:user-a': True, 'tenant_uuid': TENANT_2},
            headers_match_all=False,
        )

        deliver(consumer, {'name': 'some_event', 'tenant_uuid': TENANT_1})

        assert_that(handler.call_count, equal_to(1))

    def test_a_dispatch_without_headers_calls_no_handler(self):
        self.consumer._ConsumerMixin__dispatch('some_event', {}, None)

        self.user_a.assert_not_called()
        self.user_b.assert_not_called()


def connected_to(version):
    # the channel get_consumers receives: py-amqp keeps the broker's
    # connection.start properties, RabbitMQ's version among them
    return Mock(connection=Mock(server_properties={'version': version}))


def handler_called(subscribed, delivered, broker=None):
    consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
    if broker is not None:
        consumer.get_consumers(Mock(), broker)
    handler = Mock()
    consumer.subscribe('some_event', handler, headers=subscribed)
    deliver(consumer, {'name': 'some_event', **delivered})
    return handler.call_count


class TestBindKeysDispatchByAmqpValue(TestCase):
    # RabbitMQ's own headers match, the one a binding of the subscription's own
    # would apply: rabbit_exchange_type_headers.erl, v3.10.8 and v3.13.7

    def test_a_boolean_header_does_not_match_an_integer(self):
        assert_that(
            handler_called({'user_uuid:a': True}, {'user_uuid:a': 1}), equal_to(0)
        )
        assert_that(
            handler_called({'user_uuid:a': 1}, {'user_uuid:a': True}), equal_to(0)
        )
        assert_that(
            handler_called({'user_uuid:a': False}, {'user_uuid:a': 0}), equal_to(0)
        )

    def test_a_boolean_inside_an_array_does_not_match_an_integer(self):
        assert_that(handler_called({'tags': [True]}, {'tags': [1]}), equal_to(0))
        assert_that(
            handler_called({'tags': {'on': True}}, {'tags': {'on': 1}}), equal_to(0)
        )

    def test_equal_values_of_the_same_kind_match(self):
        for value in (True, 1, 'text', [1, 'two'], {'on': [True]}):
            assert_that(handler_called({'key': value}, {'key': value}), equal_to(1))

    def test_a_decimal_a_timestamp_or_a_void_matches_only_its_own_kind(self):
        for value in (Decimal('1.5'), datetime(2026, 11, 15)):
            assert_that(handler_called({'key': value}, {'key': value}), equal_to(1))
        assert_that(handler_called({'key': Decimal(1)}, {'key': 1}), equal_to(0))
        assert_that(handler_called({'key': 'text'}, {'key': None}), equal_to(0))

    def test_a_text_matches_its_bytes_as_both_go_on_the_wire_as_a_long_string(self):
        assert_that(handler_called({'key': 'text'}, {'key': b'text'}), equal_to(1))
        assert_that(handler_called({'key': [b'text']}, {'key': ('text',)}), equal_to(1))

    def test_a_text_with_a_lone_surrogate_matches_its_bytes_as_py_amqp_sends_it(self):
        text = 'a\ud800b'
        sent = text.encode('utf-8', 'surrogatepass')
        assert_that(handler_called({'key': text}, {'key': sent}), equal_to(1))

    def test_a_void_subscription_header_matches_the_key_whatever_its_value(self):
        assert_that(handler_called({'key': None}, {'key': 'anything'}), equal_to(1))
        assert_that(handler_called({'key': None}, {'other': 'anything'}), equal_to(0))


class TestBindKeysDispatchNumbersAsTheBrokerDoes(TestCase):
    # codex PRRT_kwDOBHUTtc63oNlU: a top-level header is compared with == up to
    # RabbitMQ 3.12 (1 equals 1.0) and with =:= from 3.13 (they differ);
    # inside an array or a table the items are typed on every version

    def test_an_integer_does_not_match_a_float_on_rabbitmq_3_13_and_later(self):
        for version in ('3.13.0', '3.13.7', '4.0.5'):
            broker = connected_to(version)
            assert_that(handler_called({'key': 1}, {'key': 1.0}, broker), equal_to(0))
            assert_that(handler_called({'key': 1.0}, {'key': 1}, broker), equal_to(0))
            assert_that(handler_called({'key': 1}, {'key': 1}, broker), equal_to(1))

    def test_an_integer_matches_a_float_before_rabbitmq_3_13(self):
        for version in ('3.10.8', '3.12.14'):
            broker = connected_to(version)
            assert_that(handler_called({'key': 1}, {'key': 1.0}, broker), equal_to(1))
            assert_that(handler_called({'key': 1.0}, {'key': 1}, broker), equal_to(1))

    def test_an_unknown_broker_tells_numbers_apart_as_rabbitmq_does_today(self):
        no_connection = Mock()
        del no_connection.connection
        for broker in (
            no_connection,
            Mock(),
            Mock(connection=Mock(server_properties={})),
            connected_to('not a version'),
            connected_to(b'3.10.8x'),
        ):
            assert_that(handler_called({'key': 1}, {'key': 1.0}, broker), equal_to(0))

    def test_the_version_is_read_where_py_amqp_keeps_it(self):
        # kombu's own channel on py-amqp's connection, never connected: the
        # properties are set as Connection._on_start sets them
        connection = pyamqp.Connection(host='localhost:1')
        connection.server_properties = {'version': '3.10.8'}
        channel = pyamqp.Channel(connection, 1)

        assert_that(broker_tells_numbers_apart(channel), equal_to(False))

    def test_the_version_may_come_as_bytes(self):
        assert_that(
            handler_called({'key': 1}, {'key': 1.0}, connected_to(b'3.10.8')),
            equal_to(1),
        )

    def test_inside_an_array_or_a_table_an_integer_is_never_a_float(self):
        for version in ('3.10.8', '4.0.5'):
            broker = connected_to(version)
            assert_that(
                handler_called({'key': [1]}, {'key': [1.0]}, broker), equal_to(0)
            )
            assert_that(
                handler_called({'key': {'n': 1}}, {'key': {'n': 1.0}}, broker),
                equal_to(0),
            )
            assert_that(handler_called({'key': [1]}, {'key': [1]}, broker), equal_to(1))

    def test_an_integer_and_a_float_bind_key_do_not_share_a_binding(self):
        # each type keeps its broker binding, so either broker version routes
        # both to the queue and the dispatcher decides
        consumer = make_headers_consumer(bind_keys=('tenant_uuid',))
        first, second = Mock(), Mock()
        consumer.subscribe('some_event', first, headers={'tenant_uuid': 1})
        consumer.subscribe('some_event', second, headers={'tenant_uuid': 1.0})
        assert_that(queue_bindings(consumer), has_length(2))

        consumer.unsubscribe('some_event', first)
        assert_that(queue_bindings(consumer), has_length(1))
        consumer.unsubscribe('some_event', second)
        assert_that(queue_bindings(consumer), empty())


class TestBindKeysStructuredValues(TestCase):
    def setUp(self):
        self.consumer = make_headers_consumer(bind_keys=('tenant_uuid',))

    def test_an_array_or_a_table_bind_key_binds_then_unbinds(self):
        for value in (['t1', 't2'], {'id': ['t1']}, ('t1',)):
            handler = Mock()
            self.consumer.subscribe(
                'some_event', handler, headers={'tenant_uuid': value}
            )
            assert_that(
                queue_bindings(self.consumer),
                equal_to(
                    [
                        (
                            '',
                            [
                                ('name', 'some_event'),
                                ('tenant_uuid', value),
                                ('x-match', 'all'),
                            ],
                        )
                    ]
                ),
            )

            assert_that(
                self.consumer.unsubscribe('some_event', handler), equal_to(True)
            )
            assert_that(queue_bindings(self.consumer), empty())

    def test_equal_structured_bind_keys_share_one_binding(self):
        first, second = Mock(), Mock()
        self.consumer.subscribe('some_event', first, headers={'tenant_uuid': ['t1']})
        self.consumer.subscribe('some_event', second, headers={'tenant_uuid': ['t1']})
        assert_that(queue_bindings(self.consumer), has_length(1))

        self.consumer.unsubscribe('some_event', first)
        assert_that(queue_bindings(self.consumer), has_length(1))
        self.consumer.unsubscribe('some_event', second)
        assert_that(queue_bindings(self.consumer), empty())

    def test_a_boolean_and_an_integer_bind_key_do_not_share_a_binding(self):
        self.consumer.subscribe('some_event', Mock(), headers={'tenant_uuid': True})
        self.consumer.subscribe('some_event', Mock(), headers={'tenant_uuid': 1})

        assert_that(queue_bindings(self.consumer), has_length(2))

    def test_a_structured_header_changed_after_subscribe_changes_nothing(self):
        # codex PRRT_kwDOBHUTtc63oNlX: the subscription keeps the values it was
        # given, so its shared key, its broker binding and its dispatch hold
        headers = {'tenant_uuid': ['t1'], 'tags': {'on': [True]}}
        handler = Mock()
        self.consumer.subscribe('some_event', handler, headers=headers)
        headers['tenant_uuid'].append('t2')
        headers['tags']['on'].append(False)

        assert_that(
            queue_bindings(self.consumer),
            equal_to([reduced('some_event', tenant_uuid=['t1'])]),
        )
        deliver(
            self.consumer,
            {'name': 'some_event', 'tenant_uuid': ['t1'], 'tags': {'on': [True]}},
        )
        assert_that(handler.call_count, equal_to(1))

        assert_that(self.consumer.unsubscribe('some_event', handler), equal_to(True))
        assert_that(queue_bindings(self.consumer), empty())
        assert_that(self.consumer._ConsumerMixin__shared_counts, equal_to({}))

    def test_unsubscribe_after_the_caller_appends_to_a_bind_key_unbinds(self):
        headers = {'tenant_uuid': ['t1']}
        handler = Mock()
        self.consumer.subscribe('some_event', handler, headers=headers)
        headers['tenant_uuid'].append('t2')

        assert_that(self.consumer.unsubscribe('some_event', handler), equal_to(True))
        assert_that(queue_bindings(self.consumer), empty())

    def test_a_header_value_amqp_cannot_carry_raises_before_any_state_changes(self):
        # py-amqp sends a str or a bytes as a long string, never a bytearray
        cannot_carry = (
            {'tenant_uuid': {'a set'}},
            {'user_uuid:a': object()},
            {'tenant_uuid': bytearray(b'text')},
            {'user_uuid:a': memoryview(b'text')},
        )
        for headers in cannot_carry:
            with self.assertRaises(TypeError):
                self.consumer.subscribe('some_event', Mock(), headers=headers)

            assert_that(self.consumer._ConsumerMixin__subscriptions, equal_to({}))
            assert_that(queue_bindings(self.consumer), empty())


def on_the_wire(headers):
    # the headers as a consumer reads them: encoded and decoded by py-amqp,
    # the field table the broker matched in between
    return loads('F', dumps('F', [headers]), 0)[0][0]


class TestBindKeysTimestampsAndDecimalsAsOnTheWire(TestCase):
    # codex PRRT_kwDOBHUTtc63ogT8: py-amqp sends a datetime as its UTC second
    # (serialization.py:393-395) and a Decimal as its scale and its unscaled
    # integer (:385-392); RabbitMQ compares those wire values

    def setUp(self):
        self.consumer = make_headers_consumer(bind_keys=('tenant_uuid',))

    def test_a_timestamp_matches_the_utc_second_it_goes_on_the_wire_as(self):
        with_microseconds = datetime(2026, 11, 15, 12, 0, 0, 500000)
        aware = datetime(2026, 11, 15, 12, 0, tzinfo=timezone(timedelta(hours=1)))
        for value in (with_microseconds, aware, [with_microseconds]):
            delivered = on_the_wire({'key': value})
            assert_that(handler_called({'key': value}, delivered), equal_to(1))

    def test_a_timestamp_does_not_match_another_second(self):
        value = datetime(2026, 11, 15, 12, 0)
        delivered = on_the_wire({'key': value + timedelta(seconds=1)})
        assert_that(handler_called({'key': value}, delivered), equal_to(0))

    def test_timestamps_of_one_second_share_one_binding(self):
        first, second = Mock(), Mock()
        at = datetime(2026, 11, 15, 12, 0, 0, 100)
        self.consumer.subscribe('some_event', first, headers={'tenant_uuid': at})
        self.consumer.subscribe(
            'some_event', second, headers={'tenant_uuid': at.replace(microsecond=0)}
        )
        assert_that(queue_bindings(self.consumer), has_length(1))

        self.consumer.unsubscribe('some_event', first)
        assert_that(queue_bindings(self.consumer), has_length(1))
        self.consumer.unsubscribe('some_event', second)
        assert_that(queue_bindings(self.consumer), empty())

    def test_decimals_of_another_scale_keep_their_own_binding(self):
        for value in (Decimal('1.0'), Decimal('1.00')):
            self.consumer.subscribe(
                'some_event', Mock(), headers={'tenant_uuid': value}
            )

        bindings = queue_bindings(self.consumer)

        assert_that(bindings, has_length(2))
        scales = sorted(
            dict(arguments)['tenant_uuid'].as_tuple().exponent
            for _, arguments in bindings
        )
        assert_that(scales, equal_to([-2, -1]))

    def test_a_decimal_matches_its_value_as_py_amqp_decodes_it(self):
        # py-amqp decodes Decimal(n) / Decimal(10 ** d) (serialization.py:108):
        # 1.0 arrives as 1, its scale is gone before the dispatcher reads it
        delivered = on_the_wire({'key': Decimal('1.0')})
        assert_that(delivered['key'].as_tuple().exponent, equal_to(0))
        assert_that(handler_called({'key': Decimal('1.0')}, delivered), equal_to(1))
        assert_that(
            handler_called(
                {'key': [Decimal('1.0')]}, on_the_wire({'key': [Decimal('1.0')]})
            ),
            equal_to(1),
        )
        in_a_table = {'key': {'d': Decimal('1.0')}}
        assert_that(handler_called(in_a_table, on_the_wire(in_a_table)), equal_to(1))
        other = on_the_wire({'key': Decimal('1.1')})
        assert_that(handler_called({'key': Decimal('1.0')}, other), equal_to(0))

    def test_a_decimal_or_a_timestamp_amqp_cannot_carry_raises_before_any_state_changes(
        self,
    ):
        # py-amqp packs a decimal's scale as an unsigned byte and its digits as
        # a signed 32-bit integer, a timestamp as an unsigned 64-bit second;
        # a datetime whose UTC time falls outside the calendar has no second
        cannot_carry = (
            {'tenant_uuid': Decimal('1E+2')},
            {'tenant_uuid': Decimal('1E-256')},
            {'user_uuid:a': datetime.min.replace(tzinfo=timezone(timedelta(hours=1)))},
            {'user_uuid:a': datetime.max.replace(tzinfo=timezone(-timedelta(hours=1)))},
            {'tenant_uuid': Decimal('NaN')},
            {'tenant_uuid': Decimal('Infinity')},
            {'tenant_uuid': Decimal(2**31)},
            {'user_uuid:a': Decimal(-(2**31) - 1)},
            {'user_uuid:a': [datetime(1969, 12, 31, 23, 59, 59)]},
        )
        for headers in cannot_carry:
            with self.assertRaisesRegex(TypeError, r'^not an AMQP (decimal|timestamp)'):
                self.consumer.subscribe('some_event', Mock(), headers=headers)

            assert_that(self.consumer._ConsumerMixin__subscriptions, equal_to({}))
            assert_that(queue_bindings(self.consumer), empty())

    def test_the_edges_py_amqp_can_carry_are_kept(self):
        for value in (
            Decimal(2**31 - 1),
            Decimal(-(2**31)),
            Decimal('0.' + '0' * 254 + '1'),
            datetime(1970, 1, 1),
        ):
            on_the_wire({'key': value})
            handler = Mock()
            self.consumer.subscribe(
                'some_event', handler, headers={'tenant_uuid': value}
            )
            assert_that(
                self.consumer.unsubscribe('some_event', handler), equal_to(True)
            )
