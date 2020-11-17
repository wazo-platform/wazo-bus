# -*- coding: utf-8 -*-
# Copyright 2012-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

logger = logging.getLogger(__name__)


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

    def publish(self, event, headers=None):
        data = self._marshaler.marshal_message(event)
        all_headers = dict(self._marshaler.metadata(event))
        all_headers.update(headers or {})
        self._publish(
            data,
            content_type=self._marshaler.content_type,
            routing_key=event.routing_key,
            headers=all_headers,
        )


class FailFastPublisher(Publisher):
    def __init__(self, producer, marshaler):
        super(FailFastPublisher, self).__init__(producer, marshaler, max_retries=2)


class LongLivedPublisher(Publisher):
    def __init__(self, producer, marshaler):
        super(LongLivedPublisher, self).__init__(
            producer,
            marshaler,
            interval_start=2,
            interval_step=2,
            interval_max=32,
        )
