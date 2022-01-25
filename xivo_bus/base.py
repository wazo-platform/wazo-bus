# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

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

    @staticmethod
    def _get_event_name(event):
        if hasattr(event, 'name'):
            return event.name
        elif isinstance(event, str):
            return event
        return None
