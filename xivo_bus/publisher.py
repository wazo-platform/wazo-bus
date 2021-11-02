# -*- coding: utf-8 -*-
# Copyright 2012-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import six
import copy

from kombu import Connection, Producer

from .base import ConsumerProducerBase, MiddlewareError
from .publishing_queue import PublishingQueue

logger = logging.getLogger(__name__)


class _BusPublisher(ConsumerProducerBase):
    def __init__(self, use_thread=True, middlewares=None, **kwargs):
        config, opts = self._split_bus_options(kwargs)

        super().__init__(use_thread=use_thread, middlewares=middlewares, **config)
        self._connection_args = self._filter_connection_args(opts)
        self._queue = (
            PublishingQueue(self._publish_factory) if self.use_thread else None
        )
        self._publish = (
            self._queue.publish if self.use_thread else self._publish_factory()
        )

    @classmethod
    def from_config(cls, config, middlewares=None, **options):
        _config = dict(copy.deepcopy(config), **options)
        if 'publish' in _config:
            _config.update(
                exchange_name=_config['publish']['exchange_name'],
                exchange_type=_config['publish']['exchange_type'],
            )

        return cls(middlewares=middlewares, **_config)

    def _publish_factory(self):
        with Connection(self._url) as connection:
            producer = Producer(connection, exchange=self._exchange, auto_declare=True)
            return connection.ensure(
                producer,
                producer.publish,
                errback=self._on_publish_error,
                **self._connection_args
            )

    @staticmethod
    def _filter_connection_args(connection_args):
        keys = {'max_retries', 'interval_start', 'interval_step', 'interval_max'}
        return dict(filter(lambda arg: arg[0] in keys, six.iteritems(connection_args)))

    def run(self):
        try:
            self._queue.run()
        except AttributeError:
            self._logger.error(
                'run() cannot be called on a publisher with use_thread=False'
            )

    def stop(self):
        if self._queue:
            self._queue.stop()
        super().stop()

    def publish(self, event, headers=None, payload=None, routing_key=None):
        headers = headers or {}
        routing_key = routing_key or getattr(event, 'routing_key', None)
        try:
            for middleware in self._middlewares:
                headers, payload = middleware(event, headers, payload)
        except Exception:
            raise MiddlewareError(middleware)
        else:
            self._publish(payload, headers=headers, routing_key=routing_key)

    def _on_publish_error(self, exc, interval):
        self._logger.error('Error: %s', exc, exc_info=1)
        self._logger.info('Retry in %s seconds...', interval)


class BusPublisherFailFast(_BusPublisher):
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
        super(BusPublisherFailFast, self).__init__(
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            middlewares=middlewares,
            use_thread=False,
            max_retries=2,
            **kwargs
        )


class BusPublisherLongLived(_BusPublisher):
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
        super(BusPublisherLongLived, self).__init__(
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            middlewares=middlewares,
            use_thread=True,
            interval_start=2,
            interval_step=2,
            interval_max=32,
            **kwargs
        )


# Deprecated, use BusPublisher instead
class Publisher(object):
    def __init__(self, producer, marshaler, **connection_args):
        self._marshaler = marshaler
        self._publish = self._new_publish(producer, connection_args)

    def _new_publish(self, producer, connection_args):
        conn = producer.connection
        return conn.ensure(
            producer,
            producer.publish,
            errback=self._on_publish_error,
            **connection_args
        )

    def _on_publish_error(self, exc, interval):
        logger.error('Error: %s', exc, exc_info=1)
        logger.info('Retry in %s seconds...', interval)

    def publish(self, event, headers=None, **kwargs):
        data = self._marshaler.marshal_message(event)
        all_headers = dict(self._marshaler.metadata(event))
        all_headers.update(headers or {})
        logger.debug('Publishing to bus: %s', event)
        self._publish(
            data,
            content_type=self._marshaler.content_type,
            routing_key=event.routing_key,
            headers=all_headers,
        )


# Deprecated, use BusPublisherFailFast instead
class FailFastPublisher(Publisher):
    def __init__(self, producer, marshaler):
        super(FailFastPublisher, self).__init__(producer, marshaler, max_retries=2)


# Deprecated, use BusPublisherLongLived instead
class LongLivedPublisher(Publisher):
    def __init__(self, producer, marshaler):
        super(LongLivedPublisher, self).__init__(
            producer, marshaler, interval_start=2, interval_step=2, interval_max=32
        )
