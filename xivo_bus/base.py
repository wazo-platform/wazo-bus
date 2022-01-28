# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from contextlib import contextmanager
from collections import namedtuple
from kombu import Exchange
from kombu.utils.url import as_url


ConnectionParams = namedtuple('ConnectionParams', 'user, password, host, port')


class Base(object):
    def __init__(
        self,
        name=None,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name='',
        exchange_type='',
        **kwargs
    ):
        self._name = name or type(self).__name__
        self._logger = logging.getLogger(type(self).__name__)
        self._connection_params = ConnectionParams(username, password, host, port)
        self._default_exchange = Exchange(name=exchange_name, type=exchange_type)

    @property
    def url(self):
        return as_url('amqp', **self._connection_params._asdict())

    @property
    def log(self):
        return self._logger

    @property
    def is_running(self):
        return False

    def marshal(self, event, headers, payload):
        return headers, payload

    def unmarshal(self, event, headers, payload):
        return headers, payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @contextmanager
    def _channel_autoretry(self, connection, retries=3):
        for count in range(retries):
            connection.ensure_connection(max_retries=1, reraise_as_library_errors=False)
            try:
                yield connection.default_channel
            except connection.connection_errors:
                self.log.error('Connection error, reconnecting (%d/%d)...', count + 1, retries)
                continue
            else:
                break
