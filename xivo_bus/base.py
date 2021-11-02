# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import inspect
import os
import six

from collections import defaultdict
from threading import Lock
from contextlib import contextmanager
from threading import Thread
from kombu import Exchange


class MiddlewareError(Exception):
    def __init__(self, middleware):
        self.message = 'Error during middleware \'{}\' execution'.format(
            type(middleware).__name__
        )


class ConsumerProducerBase(object):
    def __init__(
        self,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name=None,
        exchange_type=None,
        use_thread=True,
        middlewares=None,
        **kwargs
    ):
        if not all({username, password, host, port, exchange_name, exchange_type}):
            raise ValueError(
                '''Invalid bus configuration, please check values.
                At the very least, an exchange_name and exchange_type must be provided.'''
            )
        middlewares = middlewares or []

        self._exchange = Exchange(name=exchange_name, type=exchange_type)

        self._url = 'amqp://{username}:{password}@{host}:{port}//'.format(
            username=username, password=password, host=host, port=port
        )

        self.should_stop = False
        self.connection = None
        self._use_thread = use_thread
        self._middlewares = []
        self._thread = None

        self._init_logger()
        self.register_middleware(*(middleware for middleware in middlewares))

    def _init_logger(self):
        filename = ''
        caller = inspect.stack()[-1].filename
        if caller:
            filename, _ = os.path.splitext(os.path.basename(caller))

        self._filename = filename
        self._clsname = type(self).__name__
        self._logger = logging.getLogger(self._clsname)

    @staticmethod
    def _split_bus_options(options, **kwargs):
        bus_kwargs = {
            'username',
            'password',
            'host',
            'port',
            'exchange_name',
            'exchange_type',
            'use_thread',
            'middlewares',
        }

        config_opts = {}
        other_opts = {}
        options.update(kwargs or {})

        for key, value in six.iteritems(options):
            if key in bus_kwargs:
                config_opts[key] = value
                continue
            other_opts[key] = value
        return config_opts, other_opts

    @property
    def use_thread(self):
        return self._use_thread

    @property
    @contextmanager
    def thread(self):
        try:
            self.start()
        except RuntimeError:
            pass
        finally:
            yield
            self.stop()

    def start(self):
        if not self.use_thread:
            raise ValueError('Cannot start thread (option \'use_thread\' is disabled)')

        if self.is_running():
            raise RuntimeError(
                'Thread \'{}\' has already been started'.format(self._thread.name)
            )

        name = 'thread-{}.{}'.format(self._filename, self._clsname.lower())
        self._thread = Thread(target=self.run, name=name)
        self._logger.info("Starting AMQP thread '%s'", name)
        self._thread.start()

    def stop(self):
        if not self.is_running():
            return
        self.should_stop = True
        self._logger.info("Stopping AMQP thread '%s'", self._thread.name)
        self._thread.join()
        self._thread = None

    def is_running(self):
        return self.use_thread and self._thread and self._thread.is_alive()

    def run(self, **kwargs):
        raise NotImplementedError('Must be defined in subclass')

    def register_middleware(self, *middlewares):
        for middleware in middlewares:
            middleware = middleware() if isinstance(middleware, type) else middleware
            if not callable(middleware):
                raise ValueError(
                    'Middleware \'{}\' must be callable'.format(type(middleware))
                )
            self._middlewares.append(middleware)
            self._logger.info('Registered middleware: {}'.format(middleware))

    def unregister_middleware(self, middleware):
        for element in self._middlewares:
            if element == middleware or isinstance(element, middleware):
                self._middlewares.remove(element)
                self._logger.info('Unregistered middleware: {}'.format(middleware))
                return True
        return False

    def __repr__(self):
        return '{name}(exchange: {exchange}[{type}])'.format(
            name=self._clsname, exchange=self._exchange.name, type=self._exchange.type
        )


class EventMessageBroker(object):
    def __init__(self):
        self._subscriptions = defaultdict(list)
        self._logger = logging.getLogger(type(self).__name__)
        self._lock = Lock()

    def subscribe(self, event, handler):
        self._logger.debug(
            'Subscribed handler \'%s\' to event \'%s\'', handler.__name__, event
        )
        with self._lock:
            self._subscriptions[event].append(handler)

    def unsubscribe(self, event, handler):
        try:
            with self._lock:
                self._subscriptions[event].remove(handler)
        except ValueError:
            pass
        else:
            self._logger.debug(
                'Unsubscribed handler \'%s\' from event \'%s\'', handler.__name__, event
            )

        if not self._subscriptions[event]:
            with self._lock:
                self._subscriptions.pop(event, None)

    def dispatch(self, event, payload):
        with self._lock:
            subscribers = self._subscriptions[event].copy()

        for handler in subscribers:
            try:
                handler(payload)
            except Exception:
                self._logger.exception(
                    'Handler \'%s\' dispatching failed for event \'%s\'',
                    handler.__name__,
                    event,
                )
            continue
