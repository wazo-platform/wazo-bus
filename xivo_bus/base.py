# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import inspect
import os

from inspect import isclass
from contextlib import contextmanager
from threading import Thread
from six import raise_from
from kombu import Exchange
from kombu.utils.url import as_url

from .middlewares import Middleware


class CommonBase(object):
    context = None

    def __init__(
        self, url, exchange_name, exchange_type, use_thread=True, middlewares=None
    ):
        if not all({url, exchange_name, exchange_type}):
            raise ValueError(
                '''Invalid bus configuration, please check values.
                At the very least, an exchange_name and exchange_type must be provided.'''
            )
        self._init_logger()
        self._init_middlewares(middlewares, self.context)

        self.url = url
        self.should_stop = False
        self._exchange = Exchange(exchange_name, exchange_type)
        self._use_thread = use_thread
        self._thread = None

    @staticmethod
    def make_url(
        scheme='amqp', user='guest', password='guest', host='localhost', port=5672
    ):
        return as_url(scheme, host, port, user, password)

    def _init_middlewares(self, middlewares, context):
        self._manager = MiddlewareManager(context, self._logger)
        setattr(self, 'register_middleware', self._manager.register)
        setattr(self, 'unregister_middleware', self._manager.unregister)
        if middlewares:
            self.register_middleware(*middlewares)

    def _init_logger(self):
        filename = ''
        caller = inspect.stack()[-1].filename
        if caller:
            filename, _ = os.path.splitext(os.path.basename(caller))

        self._filename = filename
        self._clsname = type(self).__name__
        self._logger = logging.getLogger(self._clsname)

    @property
    def use_thread(self):
        return self._use_thread

    @property
    def log(self):
        return self._logger

    @property
    def exchange(self):
        return self._exchange

    @property
    @contextmanager
    def thread(self):
        try:
            self.start()
        except RuntimeError:
            pass
        try:
            yield
        finally:
            self.stop()

    def start(self, **kwargs):
        if not self.use_thread:
            raise ValueError('Cannot start thread (option \'use_thread\' is disabled)')

        if self.is_running():
            raise RuntimeError(
                'Thread \'{}\' has already been started'.format(self._thread.name)
            )

        name = 'thread-{}.{}'.format(self._filename, self._clsname.lower())
        self._thread = Thread(target=self._ensure_run, name=name, kwargs=kwargs)
        self._logger.info("Starting AMQP thread '%s'", name)
        self._thread.start()

    def stop(self):
        self.should_stop = True
        if not self.is_running():
            return
        self._logger.info("Stopping AMQP thread '%s'", self._thread.name)
        self._thread.join()
        self._thread = None
        self.should_stop = False

    def is_running(self):
        return self.use_thread and self._thread and self._thread.is_alive()

    def _ensure_run(self, **kwargs):
        while not self.should_stop:
            try:
                self.run(**kwargs)
            except Exception:
                self._logger.exception(
                    'Exception occured in thread \'%s\', restarting...',
                    self._thread.name,
                )

    def run(self, **kwargs):
        raise NotImplementedError('Must be defined in subclass')

    def register_middleware(self, *middleware):
        pass

    def unregister_middleware(self, middleware):
        pass

    def __repr__(self):
        return '<{name} (exchange: {exchange}[{type}])>'.format(
            name=self._clsname, exchange=self._exchange.name, type=self._exchange.type
        )


class MiddlewareError(Exception):
    def __init__(self, middleware):
        self.message = 'Error during middleware \'{}\' execution'.format(
            type(middleware).__name__
        )


class MiddlewareManager(object):
    _func = dict(consumer='marshal', publisher='unmarshal')

    def __init__(self, context=None, logger=None):
        self._middlewares = []
        self.log = logger or logging.getLogger(__name__)
        self.context = context

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        if context not in self._func:
            raise ValueError('Context must be either \'consumer\' or \'publisher\'')
        self._context = context

    def register(self, *middlewares):
        for middleware in middlewares:
            if isclass(middleware):
                middleware = middleware()

            if not callable(middleware) and not isinstance(middleware, Middleware):
                raise ValueError(
                    'Middleware \'{}\' is not a callable or doesn\'t inherit from Middleware class'.format(
                        middleware
                    )
                )
            self._middlewares.append(middleware)
            self.log.info('Registered middleware \'%s\'', middleware)

    def unregister(self, middleware):
        for ite in self._middlewares:
            if ite == middleware or isinstance(ite, middleware):
                self._middlewares.remove(ite)
                self.log.info('Unregistered middleware \'%s\'', middleware)
                return True
        self.log.error('No middleware \'%s\' could be found', middleware)
        return False

    def _get_middleware_op(self, middleware):
        return getattr(middleware, self._func[self.context], middleware)

    def process(self, event, headers, payload):
        for middleware in self._middlewares:
            op = self._get_middleware_op(middleware)
            try:
                headers, payload = op(event, headers, payload)
            except Exception as exc:
                raise_from(MiddlewareError(middleware), exc)
        return headers, payload
