# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from threading import Thread, Lock, Event
from datetime import datetime
from six import iteritems
from six.moves.queue import Queue as FifoQueue, Empty
from collections import namedtuple, defaultdict
from kombu import Queue, Exchange, Connection, Producer, binding as Binding
from kombu.mixins import ConsumerMixin as KombuConsumer
from amqp.exceptions import NotFound


Subscription = namedtuple('Subscription', 'handler, binding')
BusThread = namedtuple('BusThread', 'thread, on_stop, status, ready')


class ThreadableMixin(object):
    def __init__(self, **kwargs):
        super(ThreadableMixin, self).__init__(**kwargs)
        self._stop_flag = Event()

    @property
    def is_stopping(self):
        return self._stop_flag.is_set()

    @property
    def is_running(self):
        try:
            return any({bt.thread.is_alive() for bt in self.__threads})
        except AttributeError:
            return False

    @property
    def __threads(self):
        try:
            return self.__internal_threads_list
        except AttributeError:
            self.__internal_threads_list = list()
            return self.__internal_threads_list

    def __enter__(self):
        self.start()
        return super(ThreadableMixin, self).__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        super(ThreadableMixin, self).__exit__(exc_type, exc_value, traceback)

    def _register_thread(self, name, run, on_stop=None, **kwargs):
        if not callable(run):
            raise ValueError('Run must be a function')
        name = '{}:{}'.format(self._name, name)
        func = self.__wrap(run)
        barrier = Event()
        bus_thread = BusThread(
            Thread(target=func, name=name, args=(self, name, barrier), kwargs=kwargs),
            on_stop,
            None,
            barrier,
        )
        self.__threads.append(bus_thread)

    def start(self):
        if self.is_running:
            raise RuntimeError(
                '{} threads are already running'.format(len(self.__threads))
            )

        for bus_thread in self.__threads:
            bus_thread.thread.start()

        for bus_thread in self.__threads:
            bus_thread.ready.wait(timeout=3.0)
        self.log.debug('All threads started successfully...')

    def stop(self):
        self._stop_flag.set()
        for bus_thread in self.__threads:
            if bus_thread.thread.is_alive():
                self.log.debug('Stopping AMQP thread \'%s\'', bus_thread.thread.name)
                if callable(bus_thread.on_stop):
                    bus_thread.on_stop()
                bus_thread.thread.join()

    @staticmethod
    def __wrap(func):
        def wrapper(self, name, barrier, *args, **kwargs):
            self.log.debug('Started AMQP thread \'%s\'', name)
            while not self.is_stopping:
                try:
                    func(barrier, **kwargs)
                except Exception:
                    restart = ', restarting...' if not self.is_stopping else ''
                    self.log.exception(
                        'Exception occurred in thread \'%s\'%s', name, restart
                    )

        return wrapper


class ConsumerMixin(KombuConsumer):
    consumer_args = {}

    def __init__(self, subscribe=None, **kwargs):
        super(ConsumerMixin, self).__init__(**kwargs)
        name = '{name}.{id}'.format(name=self._name, id=os.urandom(3).hex())
        if subscribe:
            exchange = Exchange(subscribe['exchange_name'], subscribe['exchange_type'])

        self.__connection = Connection(self.url)
        self.__exchange = exchange if subscribe else self._default_exchange
        self.__subscriptions = defaultdict(list)
        self.__queue = Queue(
            name=name, exchange=self.__exchange, auto_delete=True, durable=False
        )
        self.__lock = Lock()

        try:
            self._register_thread('consumer', self.__run, on_stop=self.__stop)
        except AttributeError:
            pass

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
        B = Binding(self.__exchange, routing_key, headers, headers)
        self.__queue.bindings.add(B)
        try:
            with self._channel_autoretry(self.__connection) as channel:
                self.__queue.queue_declare(passive=True, channel=channel)
                B.bind(self.__queue, nowait=False, channel=channel)
        except self.__connection.connection_errors as e:
            self.log.error('Connection error while creating binding: %s', e)
        except NotFound:
            pass
        return B

    def __remove_binding(self, binding):
        self.__queue.bindings.remove(binding)
        try:
            with self._channel_autoretry(self.__connection) as channel:
                self.__queue.queue_declare(passive=True, channel=channel)
                binding.unbind(self.__queue, nowait=False, channel=channel)
        except self.__connection.connection_errors as e:
            self.log.exception('Connection error while removing binding: %s', e)
        except NotFound:
            pass

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
        headers = headers or {}
        if self.__exchange.type == 'headers':
            headers.setdefault('x-match', 'all' if headers_match_all else 'any')
        headers.setdefault('name', event)

        binding = self.__create_binding(headers, routing_key)
        subscription = Subscription(handler, binding)
        with self.__lock:
            self.__subscriptions[event].append(subscription)
        self.log.debug(
            'Registered handler \'%s\' to event \'%s\'', handler.__name__, event
        )

    def unsubscribe(self, event, handler):
        with self.__lock:
            subscriptions = self.__subscriptions[event].copy()
        try:
            for subscription in subscriptions:
                x_event = subscription.binding.arguments.get('name')
                if subscription.handler == handler and x_event == event:
                    with self.__lock:
                        self.__subscriptions[event].remove(subscription)
                    self.__remove_binding(subscription.binding)
                    self.log.debug(
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
        except Exception:
            raise
        else:
            self.__dispatch(event, payload, headers)
        finally:
            message.ack()

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        if 'ready_flag' in kwargs:
            kwargs['ready_flag'].set()

    def on_connection_error(self, exc, interval):
        super(ConsumerMixin, self).on_connection_error(exc, interval)

    def __run(self, ready_flag, **kwargs):
        with Connection(self.url) as connection:
            self.connection = connection
            super(ConsumerMixin, self).run(ready_flag=ready_flag, **self.consumer_args)

    def __stop(self):
        self.should_stop = True


class PublisherMixin(object):
    publisher_args = {}

    def __init__(self, publish=None, **kwargs):
        super().__init__(**kwargs)
        if publish:
            exchange = Exchange(publish['exchange_name'], publish['exchange_type'])
        self.__exchange = exchange if publish else self._default_exchange
        self.__connection = Connection(self.url)
        self.__publish = self.Producer(self.__connection)

    def Producer(self, connection, **connection_args):
        channel = connection.default_channel
        producer = Producer(channel, exchange=self.__exchange, auto_declare=True)
        return connection.ensure(
            producer, producer.publish, errback=self.on_publish_error, **connection_args
        )

    @staticmethod
    def _get_event_name(event):
        if hasattr(event, 'name'):
            return event.name
        elif isinstance(event, str):
            return event
        return None

    def on_publish_error(self, exc, interval):
        self.log.error('Error: %s', exc, exc_info=1)
        self.log.info('Retry in %s seconds...', interval)

    def publish(self, event, headers=None, routing_key=None, payload=None):
        headers = dict(headers or {})
        headers.setdefault('name', self._get_event_name(event))
        routing_key = routing_key or getattr(event, 'routing_key', None)

        headers, payload = self.marshal(event, headers, payload)
        self.__publish(payload, headers=headers, routing_key=routing_key)


class QueuePublisherMixin(PublisherMixin):
    def __init__(self, **kwargs):
        super(QueuePublisherMixin, self).__init__(**kwargs)
        self.__flushing = False
        self.__fifo = FifoQueue()
        try:
            self._register_thread('publisher_queue', self.__run, on_stop=self.__stop)
        except AttributeError:
            pass

    def __run(self, ready_flag, **kwargs):
        publish = None
        ready_flag.set()
        with Connection(self.url) as connection:
            while not self.is_stopping or self.__flushing:
                if not publish:
                    publish = self.Producer(connection)
                try:
                    payload, headers, routing_key = self.__fifo.get()
                except (Empty, TypeError):
                    self.__flushing = False
                    continue
                try:
                    publish(payload, headers=headers, routing_key=routing_key)
                    self.__fifo.task_done()
                except Exception:
                    self.log.exception('Error while publishing')

    def __stop(self):
        self.__flushing = True
        self.__fifo.put(None)

    def publish_soon(self, event, headers=None, routing_key=None, payload=None):
        headers = dict(headers or {})
        headers.setdefault('name', self._get_event_name(event))
        routing_key = routing_key or getattr(event, 'routing_key', None)

        headers, payload = self.marshal(event, headers, payload)
        self.__fifo.put((payload, headers, routing_key))


class WazoEventMixin(object):
    def __init__(self, service_uuid=None, **kwargs):
        super(WazoEventMixin, self).__init__(**kwargs)
        self.service_uuid = service_uuid

    def __serialize_event(self, event):
        try:
            return event.marshal()
        except AttributeError:
            self.log.exception("Received invalid event '%s'", event)
            raise ValueError('Not a valid Wazo Event')

    def __generate_metadata(self, event):
        metadata = {
            'name': event.name,
            'origin_uuid': self.service_uuid,
            'timestamp': datetime.now().isoformat(),
        }
        if hasattr(event, 'required_acl'):
            metadata['required_acl'] = event.required_acl

        return metadata

    def marshal(self, event, headers, payload):
        headers = headers or {}
        payload = {}

        headers.update(self.__generate_metadata(event))
        payload.update(headers, data=self.__serialize_event(event))
        return headers, payload

    def unmarshal(self, event, headers, payload):
        event_data = payload.pop('data')
        headers = headers or payload
        return headers, event_data
