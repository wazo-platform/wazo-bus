# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from threading import Thread
from time import monotonic
from unittest import TestCase
from unittest.mock import Mock, patch

from amqp.exceptions import AccessRefused, NotFound
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

from ..consumer import BusConsumer


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
