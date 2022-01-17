# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from collections import namedtuple
from six import iteritems
from kombu import Exchange
from kombu.utils.url import as_url

from .mixins import (
    MiddlewareMixin,
    ThreadableMixin,
    InitMixin,
    ConsumerMixin,
    QueuePublisherMixin,
)


ConnectionParams = namedtuple('ConnectionParams', 'user, password, host, port')


class Base(MiddlewareMixin):
    def __init__(
        self,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name='',
        exchange_type='',
        middlewares=None,
        **kwargs
    ):
        self._name = type(self).__name__
        self._logger = logging.getLogger(self._name)
        self._connection_params = ConnectionParams(username, password, host, port)
        self._exchange = Exchange(name=exchange_name, type=exchange_type)
        super(Base, self).__init__(middlewares=middlewares)

    def __del__(self):
        pass

    @property
    def url(self):
        return as_url('amqp', **self._connection_params._asdict())

    @property
    def log(self):
        return self._logger

    @staticmethod
    def _filter(dict_, acceptlist=None, denylist=None):
        if acceptlist and denylist:
            raise ValueError('Cannot have values for both arguments')
        if acceptlist:
            return {k: v for (k, v) in iteritems(dict_) if k in acceptlist}
        if denylist:
            return {k: v for (k, v) in iteritems(dict_) if k not in denylist}
        return dict_


class BusConnector(InitMixin, ThreadableMixin, QueuePublisherMixin, ConsumerMixin, Base):
    publisher_args = {'max_retries': 2}
