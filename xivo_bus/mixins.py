# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys

from threading import Thread, Lock, Semaphore
from inspect import isclass
from six import raise_from, iteritems
from contextlib import contextmanager
from collections import namedtuple, defaultdict
from kombu import Queue, Exchange, Connection, Producer, binding as Binding
from kombu.mixins import ConsumerMixin as KombuConsumer

from .publishing_queue import PublishingQueue
from .middlewares import Middleware, MiddlewareError


class InitMixin(object):
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
        super(InitMixin, self).__init__(
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            middlewares=middlewares,
            **kwargs
        )


class ThreadableMixin(object):
    def __init__(self, **kwargs):
        super(ThreadableMixin, self).__init__(**kwargs)
        self.should_stop = False

    @property
    def is_running(self):
        try:
            return any({thread.is_alive() for thread, _, _ in self.__threads})
        except AttributeError:
            return False

    @property
    def __threads(self):
        try:
            return self.__t
        except AttributeError:
            self.__t = list()
            return self.__t

    @property
    @contextmanager
    def threads(self):
        if not self.is_running:
            self.start()
        try:
            yield
        finally:
            self.stop()

    def start(self):
        if self.is_running:
            raise RuntimeError(
                '{} threads are already running'.format(len(self.__threads))
            )

        for thread, _, _ in self.__threads:
            thread.start()

        for _, _, barrier in self.__threads:
            barrier.acquire(blocking=True)
        self.log.debug('All thread started succesfully...')

    def stop(self):
        self.should_stop = True
        for thread, cleanup, _ in self.__threads:
            if thread.is_alive():
                self.log.info('Stopping AMQP thread \'%s\'', thread.name)
                if callable(cleanup):
                    cleanup()
                thread.join()
        self.should_stop = False

    def _register_thread(self, name, run, cleanup=None, **kwargs):
        if not callable(run):
            raise ValueError('Run must be a function')
        name = '{}:{}'.format(self._name, name)
        func = self.__wrap(run)
        barrier = Semaphore(0)
        thread = tuple(
            [
                Thread(
                    target=func, name=name, args=(self, name, barrier), kwargs=kwargs
                ),
                cleanup,
                barrier,
            ]
        )
        self.__threads.append(thread)

    @staticmethod
    def __wrap(func):
        def wrapper(self, name, barrier, *args, **kwargs):
            self.log.info('Started AMQP thread \'%s\'', name)
            barrier.release()
            while not self.should_stop:
                try:
                    func(**kwargs)
                except Exception:
                    restart = ', restarting...' if not self.should_stop else ''
                    self.log.exception(
                        'Exception occured in thread \'%s\'%s', name, restart
                    )

        return wrapper


class MiddlewareMixin(object):
    def __init__(self, middlewares=None, **kwargs):
        middlewares = middlewares or []
        super(MiddlewareMixin, self).__init__(**kwargs)

        self.__middlewares = []
        if middlewares:
            self.register_middleware(*middlewares)

    def __process(self, context, event, headers, payload):
        for middleware in self.__middlewares:
            op = getattr(middleware, context, middleware)
            try:
                headers, payload = op(event, headers, payload)
            except Exception as exc:
                raise_from(MiddlewareError(middleware), exc)
        return headers, payload

    def marshal(self, event, headers, payload):
        return self.__process('marshal', event, headers, payload)

    def unmarshal(self, event, headers, payload):
        return self.__process('unmarshal', event, headers, payload)

    def register_middleware(self, *middlewares):
        for middleware in middlewares:
            if isclass(middleware):
                middleware = middleware()
            if not callable(middleware) and not isinstance(middleware, Middleware):
                raise TypeError(
                    'Middleware registration failed: \'{}\' doesn\'t inherit from Middleware nor is a callable'.format(
                        middleware
                    )
                )
            self.__middlewares.append(middleware)
            self.log.info('Registered middleware \'%s\'', middleware)

    def unregister_middleware(self, middleware):
        for element in self.__middlewares:
            if element == middleware or (
                isclass(middleware) and isinstance(element, middleware)
            ):
                self.__middlewares.remove(element)
                self.log.info('Unregistered middleware \'%s\'', element)
                return True
        self.log.error('Middleware unregistration failed: \'%s\' not found', middleware)
        return False


Subscription = namedtuple('Subscription', 'handler binding')


class ConsumerMixin(KombuConsumer):
    consumer_args = {}

    def __init__(self, subscribe=None, **kwargs):
        super(ConsumerMixin, self).__init__(**kwargs)
        name = '{name}.{id}'.format(name=self._name, id=os.urandom(3).hex())
        if subscribe:
            exchange = Exchange(subscribe['exchange_name'], subscribe['exchange_type'])

        self.connection = Connection(self.url)
        self.__exchange = exchange if subscribe else self._exchange
        self.__subscriptions = defaultdict(list)
        self.__queue = Queue(
            name=name, exchange=self.__exchange, exclusive=True, durable=False
        )
        self.__lock = Lock()
        self.__ctrl_channel = None

        if isinstance(self, ThreadableMixin):
            self._register_thread('consumer', self.__run)

    def __configure_headers(self, event, headers, headers_match_all=True):
        headers = headers.copy() if headers else {}
        headers.setdefault('x-event', event)

        if self.__exchange.type == 'headers':
            headers.setdefault('x-match', 'all' if headers_match_all else 'any')
        return headers

    def __binding_matches(self, binding, headers):
        def discard_unused(src):
            return {k: v for (k, v) in iteritems(src) if not k.startswith('x-')}

        def match_any(src, other):
            for k, v in iteritems(src):
                if k in other and other[k] == v:
                    return True
            return False

        def match_all(src, other):
            for k, v in iteritems(src):
                if k not in other or other[k] != v:
                    return False
            return True

        if not self.__exchange.type == 'headers':
            return True

        must_match_all = binding.arguments.get('x-match', '') == 'all'
        headers = discard_unused(headers)
        binding_headers = discard_unused(binding.arguments)

        if must_match_all:
            return match_all(binding_headers, headers)
        return match_any(binding_headers, headers)

    def __create_binding(self, headers, routing_key):
        B = Binding(self.__exchange, routing_key=routing_key, arguments=headers)
        self.__queue.bindings.add(B)
        if self.__ctrl_channel:
            try:
                B.bind(self.__queue, nowait=True, channel=self.__ctrl_channel)
            except self.connection.connection_errors:
                self.log.exception('Error while installing binding')
        return B

    def __remove_binding(self, binding):
        self.__queue.bindings.remove(binding)
        if self.__ctrl_channel:
            try:
                binding.unbind(self.__queue, nowait=True, channel=self.__ctrl_channel)
            except self.connection.connection_errors:
                self.log.exception('Error while removing binding')

    def __dispatch(self, event, payload, headers=None):
        with self.__lock:
            subscriptions = self.__subscriptions[event].copy()
        for (handler, binding) in subscriptions:
            if self.__binding_matches(binding, headers):
                try:
                    handler(payload)
                except Exception:
                    self.log.exception(
                        'Handler \'%s\' for event \'%s\' failed',
                        handler.__name__,
                        event,
                    )
                continue

    def __extract_event(self, headers, payload):
        event = headers.get('name', None) or headers.get('x-event', None)
        if not event and isinstance(payload, dict):
            event = payload.get('name', None)
        return event

    def subscribe(
        self, event, handler, headers=None, routing_key=None, headers_match_all=True
    ):
        headers = self.__configure_headers(event, headers, headers_match_all)
        binding = self.__create_binding(headers, routing_key)
        subscription = Subscription(handler, binding)
        with self.__lock:
            self.__subscriptions[event].append(subscription)
        self.log.info(
            'Registered handler \'%s\' to event \'%s\'', handler.__name__, event
        )

    def unsubscribe(self, event, handler):
        with self.__lock:
            subscriptions = self.__subscriptions[event].copy()
        try:
            for subscription in subscriptions:
                x_event = subscription.binding.arguments.get('x-event')
                if subscription.handler == handler and x_event == event:
                    with self.__lock:
                        self.__subscriptions[event].remove(subscription)
                    self.__remove_binding(subscription.binding)
                    self.log.info(
                        'Unregistered handler \'%s\' from \'%s\'',
                        handler.__name__,
                        event,
                    )
                    return True
            return False
        finally:
            if not self.__subscriptions[event]:
                with self.__lock:
                    self.__subscriptions.pop(event)

    def create_connection(self):
        connection = self.connection.clone()
        self.__ctrl_channel = connection.channel()
        return connection

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=[self.__queue],
                callbacks=[self.on_message_received],
                auto_declare=True,
            )
        ]

    def on_message_received(self, body, message):
        headers = message.headers
        payload = body
        event = self.__extract_event(headers, payload)
        try:
            headers, payload = self.unmarshal(event, headers, payload)
        except MiddlewareError:
            raise
        else:
            self.__dispatch(event, payload, headers)
        finally:
            message.ack()

    def on_connection_error(self, exc, interval):
        self.__ctrl_channel = None
        super().on_connection_error(exc, interval)
        if self.should_stop:
            self.connection.close()
            sys.exit()

    def __run(self, **kwargs):
        super().run(**self.consumer_args)


class PublisherMixin(object):
    publisher_args = {}

    def __init__(self, publish=None, **kwargs):
        super().__init__(**kwargs)
        if publish:
            exchange = Exchange(publish['exchange_name'], publish['exchange_type'])
        self.__exchange = exchange if publish else self._exchange
        self.__connection = Connection(self.url)

    def __del__(self):
        self.__connection.close()
        super().__del__()

    @property
    def Producer(self):
        channel = self.__connection.default_channel
        producer = Producer(channel, exchange=self.__exchange, auto_declare=True)
        return self.__connection.ensure(
            producer,
            producer.publish,
            errback=self.on_publish_error,
            **self.publisher_args
        )

    def __get_event_name(self, event):
        if hasattr(event, 'name'):
            return event.name
        if isinstance(event, str):
            return event
        return None

    def _prepare_publish(self, event, headers=None, routing_key=None, payload=None):
        headers = headers or {}
        headers.setdefault('x-event', self.__get_event_name(event))
        routing_key = routing_key or getattr(event, 'routing_key', None)
        try:
            headers, payload = self.marshal(event, headers, payload)
        except MiddlewareError:
            raise
        return headers, payload, routing_key

    def on_publish_error(self, exc, interval):
        self.log.error('Error: %s', exc, exc_info=1)
        self.log.info('Retry in %s seconds...', interval)

    def publish(self, event, headers=None, routing_key=None, payload=None):
        headers, payload, key = self._prepare_publish(
            event, headers, routing_key, payload
        )
        self.Producer(payload, headers=headers, routing_key=key, retry=True)


class QueuePublisherMixin(PublisherMixin):
    def __init__(self, **kwargs):
        super(QueuePublisherMixin, self).__init__(**kwargs)
        self.__queue = PublishingQueue(self.__factory)
        self._register_thread('publisher_longlived', self.__run, cleanup=self.__stop)

    def __run(self, **kwargs):
        self.__queue.run()

    def __stop(self):
        self.__queue.flush_and_stop()

    def __factory(self):
        return self.Producer

    def publish_soon(self, event, headers=None, routing_key=None, payload=None):
        headers, payload, key = self._prepare_publish(
            event, headers, routing_key, payload
        )
        self.__queue.publish(payload, headers, key)
