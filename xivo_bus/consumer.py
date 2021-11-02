# Copyright 2020-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import copy
import os

from kombu import Connection, Queue, binding as Binding
from kombu.exceptions import NotBoundError
from kombu.mixins import ConsumerMixin

from .base import ConsumerProducerBase as Base, EventMessageBroker, MiddlewareError


class BusConsumer(ConsumerMixin, Base):
    def __init__(
        self,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name=None,
        exchange_type=None,
        middlewares=None,
        **kwargs
    ):
        super().__init__(
            username,
            password,
            host,
            port,
            exchange_name,
            exchange_type,
            True,
            middlewares,
        )
        self._is_running = False
        self._broker = EventMessageBroker()
        self._bindings = set([])

        queue_name = '{module}.{name}-{id}'.format(
            module=self._filename, name=self._clsname, id=self._generate_random_hex(3)
        )
        self._queue = Queue(name=queue_name, durable=False, auto_delete=True)

    @staticmethod
    def _generate_random_hex(size):
        return os.urandom(size).hex()

    @classmethod
    def from_config(cls, config, middlewares=None, **options):
        _config = dict(copy.deepcopy(config), **options)
        if 'subscribe' in _config:
            _config.update(
                exchange_name=_config['subscribe']['exchange_name'],
                exchange_type=_config['subscribe']['exchange_type'],
            )

        return cls(middlewares=middlewares, **_config)

    def get_consumers(self, Consumer, channel):
        self._exchange(channel).declare()
        self._queue(channel).declare()

        return [
            Consumer(
                queues=[self._queue],
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
        try:
            with Connection(self._url) as connection:
                self.connection = connection
                super().run(**consume_args)
        except Exception:
            self._logger.exception('Thread exited')

    def is_running(self):
        return super().is_running() and self._is_running

    def _on_message_received(self, body, message):
        headers = message.headers
        event = headers.get('name', None) or body.get('name')
        payload = body
        try:
            for middleware in self._middlewares:
                headers, payload = middleware(event, headers, payload)
        except Exception:
            raise MiddlewareError(middleware)
        else:
            self._broker.dispatch(event, payload)
        finally:
            message.ack()

    def register_event_handler(
        self, event, handler, headers=None, headers_match_all=True, routing_key=None
    ):
        if self._exchange.type == 'headers' and routing_key:
            self._logger.warning(
                'Exchange \'%s\' is using headers, routing_key will not be used.',
                self._exchange.name,
            )

        if self._exchange.type == 'topic' and headers:
            self._logger.warning(
                'Exchange \'%s\' is using routing_key, headers will not be used.'
            )

        headers = headers or {}
        headers.setdefault('name', event)
        headers.setdefault('x-match', 'all' if headers_match_all else 'any')
        B = Binding(self._exchange, routing_key, headers)

        try:
            with self.establish_connection() as connection:
                with connection.channel() as channel:
                    self._queue.bind_to(
                        B.exchange, B.routing_key, B.arguments, channel=channel
                    )
        except AttributeError:
            pass
        self._queue.bindings.add(B)
        self._broker.subscribe(event, handler)
        self._logger.info(
            'Registered on event \'%s\' (handler: \'%s\')', event, handler.__name__
        )

    def unregister_event_handler(self, event, handler):
        for B in self._queue.bindings:
            if B.arguments.get('name') != event:
                continue

            try:
                with self.establish_connection() as connection:
                    with connection.channel() as channel:
                        self._queue.unbind_from(
                            B.exchange, B.routing_key, B.arguments, channel=channel
                        )
            except (AttributeError, NotBoundError):
                self._logger.error(
                    'Failed to unregister event \'%s\'', event, exc_info=1
                )
                return False
            self._queue.bindings.remove(B)
            self._broker.unsubscribe(event, handler)
            self._logger.info(
                'Unregistered event \'%s\' (handler: \'%s\')', event, handler.__name__
            )
            return True
        self._logger.error(
            'Failed to unregister event \'%s\', handler not found.', event
        )
        return False
