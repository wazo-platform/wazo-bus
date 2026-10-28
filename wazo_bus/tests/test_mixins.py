# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from threading import Thread
from time import monotonic
from unittest import TestCase
from unittest.mock import Mock, patch

from amqp.exceptions import NotFound
from hamcrest import (
    assert_that,
    equal_to,
    has_item,
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

    def test_an_unbind_not_found_counts_as_removed_without_ending_the_batch(self):
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

        assert_that([name for name, _ in calls], equal_to(['unbind', 'unbind', 'bind']))
        failed_channel = calls[0][1]
        assert_that(calls[1][1], is_not(same_instance(failed_channel)))
        assert_that(calls[2][1], is_not(same_instance(failed_channel)))
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
