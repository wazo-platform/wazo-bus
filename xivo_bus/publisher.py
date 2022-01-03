# -*- coding: utf-8 -*-
# Copyright 2012-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import six

from abc import ABCMeta
from six import add_metaclass
from kombu import Connection, Producer

from .base import CommonBase, MiddlewareError
from .publishing_queue import PublishingQueue

logger = logging.getLogger(__name__)


def _filter_args(keywords, args):
    return dict(filter(lambda a: a[0] in keywords, six.iteritems(args)))


@add_metaclass(ABCMeta)
class PublisherBase(CommonBase):
    context = 'publisher'

    def __init__(
        self,
        exchange_name,
        exchange_type,
        user='guest',
        password='guest',
        host='localhost',
        port=5672,
        use_thread=True,
        middlewares=None,
        **connection_args
    ):
        url = self.make_url(user=user, password=password, host=host, port=port)
        super(PublisherBase, self).__init__(
            url, exchange_name, exchange_type, use_thread, middlewares
        )

        self._connection_args = _filter_args(
            {'max_retries', 'interval_start', 'interval_step', 'interval_max'},
            connection_args,
        )

        self._publish = self._publish_factory()
        if use_thread:
            self._queue = PublishingQueue(self._publish_factory)
            self._publish = self._queue.publish

    @classmethod
    def from_config(cls, config, middlewares=None):
        config = config.copy()
        if 'publish' in config:
            config['exchange_name'] = config['publish']['exchange_name']
            config['exchange_type'] = config['publish']['exchange_type']
        exchange_name = config.pop('exchange_name')
        exchange_type = config.pop('exchange_type')
        return cls(exchange_name, exchange_type, middlewares=middlewares, **config)

    def _publish_factory(self):
        with Connection(self.url) as connection:
            producer = Producer(connection, exchange=self.exchange, auto_declare=True)
            return connection.ensure(
                producer,
                producer.publish,
                errback=self._on_publish_error,
                **self._connection_args
            )

    def run(self):
        try:
            self._queue.run()
        except AttributeError:
            self._logger.error(
                'run() cannot be called on a publisher with use_thread=False'
            )
            self.stop()

    def stop(self):
        if self._queue:
            self._queue.stop()
        super(PublisherBase, self).stop()

    def publish(self, event, headers=None, payload=None, routing_key=None):
        headers = headers or {}
        routing_key = routing_key or getattr(event, 'routing_key', None)
        try:
            headers, payload = self._manager.process(event, headers, payload)
        except MiddlewareError:
            raise
        else:
            self._publish(payload, headers=headers, routing_key=routing_key)

    def _on_publish_error(self, exc, interval):
        self.log.error('Error: %s', exc, exc_info=1)
        self.log.info('Retry in %s seconds...', interval)


class BusPublisherFailFast(PublisherBase):
    def __init__(
        self,
        exchange_name,
        exchange_type,
        user='guest',
        password='guest',
        host='localhost',
        port=5672,
        middlewares=None,
    ):
        super(BusPublisherFailFast, self).__init__(
            exchange_name,
            exchange_type,
            user=user,
            password=password,
            host=host,
            port=port,
            middlewares=middlewares,
            use_thread=False,
            max_retries=2,
        )


class BusPublisherLongLived(PublisherBase):
    def __init__(
        self,
        exchange_name,
        exchange_type,
        user='guest',
        password='guest',
        host='localhost',
        port=5672,
        middlewares=None,
    ):
        super(BusPublisherLongLived, self).__init__(
            exchange_name,
            exchange_type,
            user=user,
            password=password,
            host=host,
            port=port,
            middlewares=middlewares,
            use_thread=True,
            interval_start=2,
            interval_step=2,
            interval_max=32,
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
