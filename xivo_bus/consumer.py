# Copyright 2020-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import logging

from collections import defaultdict, namedtuple
from threading import Lock
from kombu import Connection, Queue, binding as Binding
from kombu.exceptions import NotBoundError
from kombu.mixins import ConsumerMixin

from .base import CommonBase as Base, MiddlewareError

Subscription = namedtuple('Subscription', ['handler', 'binding'])


class BusConsumer(ConsumerMixin, Base):
    context = 'consumer'

    def __init__(
        self,
        exchange_name=None,
        exchange_type=None,
        user='guest',
        password='guest',
        host='localhost',
        port=5672,
        middlewares=None,
    ):
        url = self.make_url(user=user, password=password, host=host, port=port)
        super().__init__(
            url, exchange_name, exchange_type, use_thread=True, middlewares=middlewares
        )

        service_name = '{}.{}'.format(self._filename, self._clsname)
        self.connection = None
        self._is_running = False
        self._registrar = EventRegistrar(
            self, name=service_name, durable=False, auto_delete=True
        )

    @classmethod
    def from_config(cls, config, middlewares=None):
        config = config.copy()
        if 'subscribe' in config:
            config['exchange_name'] = config['subscribe']['exchange_name']
            config['exchange_type'] = config['subscribe']['exchange_type']
        exchange_name = config.pop('exchange_name')
        exchange_type = config.pop('exchange_type')
        return cls(exchange_name, exchange_type, middlewares=middlewares, **config)

    def get_consumers(self, Consumer, channel):
        self.exchange(channel).declare()
        self._registrar.queue(channel).declare()

        return [
            Consumer(
                queues=[self._registrar.queue],
                callbacks=[self._on_message_received],
                auto_declare=False,
            )
        ]

    def on_connection_error(self, exc, interval):
        super().on_connection_error(exc, interval)
        self._is_running = False

    def on_connection_revived(self):
        super().on_connection_revived()
        self._is_running = True

    def run(self, **consume_args):
        with Connection(self.url) as connection:
            self.connection = connection
            super().run(**consume_args)

    def is_running(self):
        return super().is_running() and self._is_running

    def _on_message_received(self, body, message):
        headers = message.headers
        event = headers.get('name', None) or body.get('name', None)
        payload = body
        try:
            headers, payload = self._manager.process(event, headers, payload)
        except MiddlewareError:
            raise
        else:
            self._registrar.dispatch(event, payload)
        finally:
            message.ack()

    def register_event_handler(
        self, event, handler, headers=None, routing_key=None, headers_match_all=True
    ):
        self._registrar.subscribe(
            event, handler, headers, headers_match_all, routing_key
        )

    def unregister_event_handler(self, event, handler):
        return self._registrar.unsubscribe(event, handler)


class EventRegistrar(object):
    def __init__(self, provider, name=None, **queue_kwargs):
        if name:
            name = '{name}-{id}'.format(name=name, id=os.urandom(3).hex())

        self._provider = provider
        self._subscriptions = defaultdict(list)
        self._lock = Lock()
        self._queue = Queue(name=name, exchange=None, **queue_kwargs)

    @property
    def log(self):
        try:
            return self._provider.log
        except AttributeError:
            logging.getLogger(__name__)

    @property
    def queue(self):
        return self._queue

    @property
    def exchange(self):
        return self._provider.exchange

    def _configure_headers(self, event, headers, routing_key, headers_match_all=True):
        headers = dict(**headers)
        headers.setdefault('x-event', event)
        exchange = self.exchange

        if exchange.type == 'headers':
            headers.setdefault('x-match', 'all' if headers_match_all else 'any')
            if routing_key:
                self.log.warning(
                    'Exchange \'%s\' is using headers, routing_key will not be used.',
                    exchange.name,
                )
        elif exchange.type == 'topic' and headers:
            self.log.warning(
                'Exchange \'%s\' is using routing_key, headers will not be used.',
                exchange.name,
            )
        return headers

    def _create_binding(self, headers, routing_key):
        B = Binding(self.exchange, routing_key=routing_key, arguments=headers)
        self._queue.bindings.add(B)
        try:
            with self._provider.establish_connection() as connection:
                with connection.channel() as channel:
                    self._queue.bind_to(
                        B.exchange, B.routing_key, B.arguments, channel=channel
                    )
        except NotBoundError:
            pass
        return B

    def _remove_binding(self, binding):
        self._queue.bindings.remove(binding)
        try:
            with self._provider.establish_connection() as connection:
                with connection.channel() as channel:
                    self._queue.unbind_from(
                        binding.exchange,
                        binding.routing_key,
                        binding.arguments,
                        channel=channel,
                    )
        except NotBoundError:
            pass

    def subscribe(
        self, event, handler, headers=None, headers_match_all=True, routing_key=None
    ):
        headers = self._configure_headers(
            event, headers, routing_key, headers_match_all
        )
        subscription = Subscription(handler, self._create_binding(headers, routing_key))

        with self._lock:
            self._subscriptions[event].append(subscription)
        self.log.info(
            'Registered handler \'%s\' to event \'%s\'', handler.__name__, event
        )

    def unsubscribe(self, event, handler):
        with self._lock:
            subscriptions = self._subscriptions[event].copy()

        try:
            for subscription in subscriptions:
                if (
                    subscription.handler == handler
                    and subscription.binding.arguments.get('x-event', None) == event
                ):
                    with self._lock:
                        self._subscriptions[event].remove(subscription)
                    self._remove_binding(subscription.binding)
                    self.log.info(
                        'Unregistered handler \'%s\' from \'%s\'', handler, event
                    )
                    return True
            return False
        finally:
            if not self._subscriptions[event]:
                with self._lock:
                    self._subscriptions.pop(event, None)

    def dispatch(self, event, payload):
        with self._lock:
            subscribers = self._subscriptions[event].copy()

        for (handler, _) in subscribers:
            try:
                handler(payload)
            except Exception:
                self.log.exception(
                    'Handler \'%s\' dispatching failed for event \'%s\'',
                    handler.__name__,
                    event,
                )
            continue
