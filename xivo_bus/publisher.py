# Copyright 2012-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from .base import Base
from .mixins import QueuePublisherMixin, PublisherMixin, ThreadableMixin, WazoEventMixin

logger = logging.getLogger(__name__)


class BusPublisher(WazoEventMixin, PublisherMixin, Base):
    def __init__(
        self,
        name=None,
        service_uuid=None,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name='',
        exchange_type='',
        **kwargs
    ):
        super(BusPublisher, self).__init__(
            name=name,
            service_uuid=service_uuid,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            **kwargs
        )


# Deprecated, thread should be avoided to respect WPEP-0004
class BusPublisherWithQueue(WazoEventMixin, ThreadableMixin, QueuePublisherMixin, Base):
    def __init__(
        self,
        name=None,
        service_uuid=None,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name='',
        exchange_type='',
        **kwargs
    ):
        super(BusPublisherWithQueue, self).__init__(
            name=name,
            service_uuid=service_uuid,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            **kwargs
        )


# Deprecated, use BusPublisher instead
class Publisher(object):

    def __init__(self, producer, marshaler, **connection_args):
        self._producer = producer
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

    def is_connected(self):
        return self._producer.connection.connected


# Deprecated, use BusPublisher instead
class FailFastPublisher(Publisher):
    def __init__(self, producer, marshaler):
        super(FailFastPublisher, self).__init__(producer, marshaler, max_retries=2)


# Deprecated, use BusPublisher instead
class LongLivedPublisher(Publisher):
    def __init__(self, producer, marshaler):
        super(LongLivedPublisher, self).__init__(
            producer, marshaler, interval_start=2, interval_step=2, interval_max=32
        )
