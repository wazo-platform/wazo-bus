# Copyright 2021-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import datetime
from queue import Empty, Queue
from threading import Condition, Event, Lock, Thread, current_thread, main_thread
from time import monotonic
from typing import Any, ClassVar, NamedTuple, Protocol, Self

from amqp.exceptions import NotFound
from kombu import Connection, Consumer, Message, Producer
from kombu import Queue as AMQPQueue
from kombu import binding as Binding
from kombu.exceptions import OperationalError
from kombu.mixins import ConsumerMixin as KombuConsumer
from kombu.transport.base import StdChannel

from .base import BaseProtocol
from .collectd.common import CollectdEvent
from .resources.common.abstract import EventProtocol

EventHandlerType = Callable[[dict], None]
ThreadTargetType = Callable[..., None]
ThreadOnStopType = Callable[[], None]


class BusThread(NamedTuple):
    thread: Thread
    on_stop: ThreadOnStopType | None
    ready_flag: Event


class Subscription(NamedTuple):
    handler: EventHandlerType
    binding: Binding


class ThreadableProtocol(Protocol):
    @property
    def is_stopping(self) -> bool:
        ...

    def _register_thread(
        self,
        name: str,
        run: ThreadTargetType,
        on_stop: ThreadOnStopType | None,
        **kwargs: Any,
    ) -> Thread:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...


class ThreadableMixin(BaseProtocol):
    '''
    Mixin to provide methods for easy thread creation/management

    Public attributes:
        * `is_running`:
            Returns True if threads are alive and running

    Public methods:
        * `start`:
            Starts execution of registered thread
        * `stop`:
            Kill all running threads

    Private methods:
        * `_register_thread`:
            Allows another mixin to register a thread for execution
    '''

    def __init__(self, **kwargs: Any):
        self.__internal_threads_list: list[BusThread] = list()
        self.__stop_flag = Event()
        # NOTE(clanglois): Mixin expects a parent class to provide __init__ implementation
        super().__init__(**kwargs)  # type: ignore[safe-super]

    @property
    def is_stopping(self) -> bool:
        return self.__stop_flag.is_set()

    @property
    def is_running(self) -> bool:
        status = all({bus_thread.thread.is_alive() for bus_thread in self.__threads})
        return super().is_running and status  # type: ignore[safe-super]

    @property
    def __threads(self) -> list[BusThread]:
        return self.__internal_threads_list

    def __enter__(self) -> Self:
        self.start()
        return super().__enter__()

    def __exit__(self, *args: Any) -> None:
        self.stop()
        # NOTE(clanglois): Mixin expects a parent class to provide __exit__ implementation
        super().__exit__(*args)  # type: ignore[safe-super]

    def _register_thread(
        self,
        name: str,
        run: ThreadTargetType,
        on_stop: ThreadOnStopType | None = None,
        **kwargs: Any,
    ) -> Thread:
        if not callable(run):
            raise ValueError('Run must be a function')
        ready_flag = Event()
        bus_thread = BusThread(
            Thread(
                target=self.__wrap_thread(run),
                name=f'{self._name}:{name}',
                args=(self, name, ready_flag),
                kwargs=kwargs,
            ),
            on_stop,
            ready_flag,
        )
        self.__threads.append(bus_thread)
        return bus_thread.thread

    def start(self) -> None:
        if self.is_running:
            raise RuntimeError(f'{len(self.__threads)} threads are already running')

        for bus_thread in self.__threads:
            bus_thread.thread.start()

        for bus_thread in self.__threads:
            bus_thread.ready_flag.wait(timeout=3.0)
        self.log.debug('All threads started successfully...')

    def stop(self) -> None:
        self.__stop_flag.set()
        for bus_thread in self.__threads:
            if bus_thread.thread.is_alive():
                self.log.debug('Stopping AMQP thread \'%s\'', bus_thread.thread.name)
                if callable(bus_thread.on_stop):
                    bus_thread.on_stop()
                bus_thread.thread.join()

    @staticmethod
    def __wrap_thread(func: ThreadTargetType) -> ThreadTargetType:
        def wrapper(self: Self, name: str, ready_flag: Event, **kwargs: Any) -> None:
            self.log.debug('Started AMQP thread \'%s\'', name)
            while not self.is_stopping:
                try:
                    func(ready_flag, **kwargs)
                except Exception:
                    restart = ', restarting...' if not self.is_stopping else ''
                    self.log.exception(
                        'Exception occurred in thread \'%s\'%s', name, restart
                    )

        return wrapper


class ConsumerMixin(KombuConsumer, BaseProtocol):
    '''
    Mixin to provide RabbitMQ message consuming capabilities.

    Bindings are reconciled against the broker from the consumer thread on
    every `on_iteration` tick. `subscribe`/`unsubscribe` mutate the desired
    state and return immediately; convergence happens within one
    `safety_interval`. Callers that need a barrier (tests, batched
    setup/teardown) can use `wait_synchronized()`.

    Public methods:
        * `consumer_connected`:
            Returns whether the consumer is connected to RabbitMQ or not
        * `subscribe`:
            Install a handler for the specified event
        * `unsubscribe`:
            Uninstall a handler for the specified event
        * `wait_synchronized`:
            Block until desired bindings are live at the broker
    '''

    consumer_args: ClassVar[dict] = {'safety_interval': 0.2}

    def __init__(self, **kwargs: Any):
        # NOTE(clanglois): Mixin expects a parent class to provide __init__ implementation
        super().__init__(**kwargs)  # type: ignore[safe-super]
        self.__subscriptions: dict[str, list[Subscription]] = {}
        self.__bindings: set[Binding] = set()
        self.__queue: AMQPQueue | None = None
        self.__lock = Lock()
        self.__synced = Condition(self.__lock)
        self.__thread: Thread | None = None
        if hasattr(self, '_register_thread'):
            self.__thread = self._register_thread(
                'consumer', self.__thread_run, self.__thread_stop
            )

        self.create_connection()
        self.log.debug('setting consuming exchange as \'%s\'', self._exchange)

    def consumer_connected(self) -> bool:
        is_running = self.__thread.is_alive() if self.__thread is not None else True
        return bool(is_running and self.connection.connected)

    def __is_synced(self) -> bool:
        if self.__queue is None:
            return not self.__bindings
        return self.__bindings == self.__queue.bindings

    def wait_synchronized(self, timeout: float = 5.0) -> bool:
        deadline = monotonic() + timeout
        with self.__synced:
            while True:
                if self.is_stopping:
                    return False
                if self.__is_synced():
                    return True
                remaining = deadline - monotonic()
                if remaining <= 0:
                    return False
                self.__synced.wait(timeout=remaining)

    def on_iteration(self) -> None:
        if self.__queue is None:
            return

        with self.__synced:
            active_before = set(self.__queue.bindings)
            to_add = self.__bindings - active_before
            to_remove = active_before - self.__bindings

        if not to_add and not to_remove:
            return

        self.__apply_binding_changes(to_add, to_remove)

        with self.__synced:
            if self.__queue.bindings != active_before:
                self.__synced.notify_all()

    @contextmanager
    def __open_channel(self) -> Iterator[StdChannel]:
        channel = self.connection.channel()
        try:
            yield channel
        finally:
            try:
                channel.close()
            except Exception:
                self.log.debug('Ignoring error while closing channel', exc_info=True)

    def __apply_binding_changes(
        self, to_add: set[Binding], to_remove: set[Binding]
    ) -> None:
        if self.__queue is None:
            return

        errors = self.connection.connection_errors + self.connection.channel_errors
        added: set[Binding] = set()
        removed: set[Binding] = set()

        with self.__open_channel() as channel:
            for binding in to_add:
                try:
                    binding.bind(self.__queue, channel=channel)
                except NotFound as exc:
                    self.log.warning(
                        'Queue %s gone while binding %s, reconnecting: %s',
                        self.__queue.name,
                        binding,
                        exc,
                    )
                    raise
                except errors as exc:
                    self.log.warning('Failed to bind %s, will retry: %s', binding, exc)
                    continue
                added.add(binding)

            for binding in to_remove:
                try:
                    binding.unbind(self.__queue, channel=channel)
                except NotFound as exc:
                    self.log.warning(
                        'Queue %s gone while unbinding %s, reconnecting: %s',
                        self.__queue.name,
                        binding,
                        exc,
                    )
                    raise
                except errors as exc:
                    self.log.warning(
                        'Failed to unbind %s, will retry: %s', binding, exc
                    )
                    continue
                removed.add(binding)

        with self.__synced:
            self.__queue.bindings |= added
            self.__queue.bindings -= removed

    def __dispatch(
        self, event_name: str, payload: dict, headers: dict | None = None
    ) -> None:
        with self.__synced:
            subscriptions = tuple(self.__subscriptions.get(event_name, ()))

        if subscriptions:
            self.log.debug(
                'Received bus event: name=%s, headers=%s, payload=%s',
                event_name,
                headers,
                payload,
            )

        for handler, _ in subscriptions:
            try:
                handler(payload)
            except Exception:
                self.log.exception(
                    'Handler \'%s\' for event \'%s\' failed',
                    getattr(handler, '__name__', handler),
                    event_name,
                )

    def __extract_event_from_message(self, message: Message) -> tuple[str, dict, dict]:
        event_name = None
        headers = dict(message.headers)
        payload = message.payload
        if isinstance(payload, dict):
            payload = dict(payload)

        if 'name' in headers:
            event_name = headers['name']
        elif isinstance(payload, dict) and 'name' in payload:
            event_name = payload['name']
        else:
            raise ValueError('Received invalid message; no event name could be found.')
        return event_name, headers, payload

    def subscribe(
        self,
        event_name: str,
        handler: EventHandlerType,
        headers: dict | None = None,
        routing_key: str | None = None,
        headers_match_all: bool = True,
    ) -> None:
        headers = dict(headers or {})
        headers.update(name=event_name)

        if self._exchange.type == 'headers':
            headers.setdefault('x-match', 'all' if headers_match_all else 'any')

        binding = Binding(self._exchange, routing_key, headers, headers)
        subscription = Subscription(handler, binding)

        with self.__synced:
            self.__subscriptions.setdefault(event_name, []).append(subscription)
            self.__bindings.add(binding)

        self.log.debug(
            'Registered handler \'%s\' to event \'%s\'',
            getattr(handler, '__name__', handler),
            event_name,
        )

    def unsubscribe(
        self,
        event_name: str,
        handler: EventHandlerType,
    ) -> bool:
        with self.__synced:
            subscriptions = self.__subscriptions.get(event_name)
            if subscriptions is None:
                return False

            matching = next((s for s in subscriptions if s.handler == handler), None)
            if matching is None:
                return False

            subscriptions.remove(matching)
            self.__bindings.discard(matching.binding)

            if not subscriptions:
                self.__subscriptions.pop(event_name)

        self.log.debug(
            'Unregistered handler \'%s\' from \'%s\'',
            getattr(handler, '__name__', handler),
            event_name,
        )
        return True

    def get_consumers(
        self, Consumer: type[Consumer], channel: StdChannel
    ) -> list[Consumer]:
        with self.__synced:
            self.__queue = AMQPQueue(
                name=f'{self._name}.{os.urandom(3).hex()}',
                exclusive=True,
                auto_delete=True,
                durable=False,
                bindings=set(self.__bindings),
            )

        self._exchange.bind(channel).declare()
        return [
            Consumer(
                queues=[self.__queue],
                callbacks=[self.__on_message_received],
                auto_declare=True,
            )
        ]

    def __on_message_received(self, _body: Any, message: Message) -> None:
        try:
            event_name, headers, payload = self.__extract_event_from_message(message)
            if event_name not in self.__subscriptions:
                return
            headers, payload = self._unmarshal(event_name, headers, payload)
            self.__dispatch(event_name, payload, headers)
        except Exception:
            self.log.exception('Failed to process message')
            raise
        finally:
            message.ack()

    def on_connection_error(self, exc: Exception, interval: str) -> None:
        self.log.error(
            'Broker connection error: %s, trying to reconnect in %s seconds...',
            exc,
            interval,
        )
        if self.should_stop:
            if current_thread() != main_thread():
                raise SystemExit
            self.connection.release()

    def create_connection(self) -> Connection:
        self.connection = Connection(self.url)
        return self.connection

    @property
    def should_stop(self) -> bool:
        return getattr(self, 'is_stopping', True)

    def on_consume_ready(
        self,
        connection: Connection,
        channel: Any,
        consumers: list[Consumer],
        **kwargs: Any,
    ) -> None:
        if 'ready_flag' in kwargs:
            ready_flag = kwargs.pop('ready_flag')
            ready_flag.set()
        with self.__synced:
            self.__synced.notify_all()

    def __thread_run(self, ready_flag: Event, **kwargs: Any) -> None:
        super().run(ready_flag=ready_flag, **self.consumer_args)

    def __thread_stop(self) -> None:
        with self.__synced:
            self.__synced.notify_all()


class PublisherMixin(BaseProtocol):
    '''
    Mixin providing RabbitMQ message publishing capabilities

    Methods:
        * `publisher_connected`:
            Returns whether publisher is connected to RabbitMQ or not
        * `publish`:
            publish an event immediately to the bus
    '''

    publisher_args: ClassVar[dict] = {
        'max_retries': 2,
    }

    def __init__(
        self,
        **kwargs: Any,
    ):
        # NOTE(clanglois): Mixin expects a parent class to provide __init__ implementation
        super().__init__(**kwargs)  # type: ignore[safe-super]
        self.__connection = Connection(self.url, transport_options=self.publisher_args)
        self.__lock = Lock()
        self.log.debug('setting publishing exchange as \'%s\'', self._exchange)

    def publisher_connected(self) -> bool:
        return self.__connection.connected

    @contextmanager
    def Producer(
        self, connection: Connection, **connection_args: Any
    ) -> Iterator[Callable]:
        producer = Producer(connection, exchange=self._exchange, auto_declare=True)
        yield connection.ensure(
            producer, producer.publish, errback=self.on_publish_error, **connection_args
        )

    def on_publish_error(self, exc: Exception, interval: int | str) -> None:
        self.log.error('Publish error: %s', exc, exc_info=True)
        self.log.info('Retry in %s seconds...', interval)

    def publish(
        self,
        event: EventProtocol,
        headers: dict | None = None,
        routing_key: str | None = None,
        payload: dict | None = None,
    ) -> None:
        headers, payload, routing_key = self._marshal(
            event, headers, payload, routing_key=routing_key
        )
        content_type = getattr(self, 'content_type', None)
        with self.__lock:
            with self.Producer(self.__connection, **self.publisher_args) as publish:
                publish(
                    payload,
                    headers=headers,
                    routing_key=routing_key,
                    content_type=content_type,
                )
        self.log.debug('Published %s', str(event))


class QueuePublisherMixin(PublisherMixin, ThreadableProtocol):
    '''
    Mixin to provide publishing capabilities, including ability to publish
    through a thread

    **Note: Exclusive with PublisherMixin**

    Public methods:
        * `publisher_connected`:
            Returns publisher's connection state to rabbitmq
        * `queue_publisher_connected`:
            Returns threaded publisher's connection state to rabbitmq
        * `publish`:
            Publish an event immediately to the bus without queueing
        * `publish_soon`:
            Queue an event to be processed by the publishing thread
    '''

    queue_publisher_args: ClassVar[dict] = {
        'interval_start': 2,
        'interval_step': 2,
        'interval_max': 32,
    }

    def __init__(self, **kwargs: Any) -> None:
        retry_policy = self.queue_publisher_args
        super().__init__(**kwargs)
        self.__flushing: bool = False
        self.__fifo: Queue = Queue()
        self.__connection = Connection(self.url, transport_options=retry_policy)
        self.__thread: Thread | None = None

        if hasattr(self, '_register_thread'):
            self.__thread = self._register_thread(
                'publisher_queue', self.__thread_run, self.__thread_stop
            )

    def queue_publisher_connected(self) -> bool:
        is_running = self.__thread.is_alive() if self.__thread is not None else True
        return bool(self.__connection.connected and is_running)

    def __thread_run(self, ready_flag: Event, **kwargs: Any) -> None:
        ready_flag.set()
        retry_policy = self.queue_publisher_args

        with self.__connection:
            while not self.is_stopping or self.__flushing:
                try:
                    payload, headers, routing_key = self.__fifo.get()
                except (Empty, TypeError):
                    self.__flushing = False
                    continue
                try:
                    with self.Producer(self.__connection, **retry_policy) as publish:
                        publish(payload, headers=headers, routing_key=routing_key)
                except OperationalError as exc:
                    self.log.error('Publishing queue error: %s', exc, exc_info=True)
                else:
                    self.__fifo.task_done()

    def __thread_stop(self) -> None:
        self.__flushing = True
        self.__fifo.put(None)

    def publish_soon(
        self,
        event: EventProtocol,
        headers: dict | None = None,
        routing_key: str | None = None,
        payload: dict | None = None,
    ) -> None:
        headers, payload, routing_key = self._marshal(
            event, headers, payload, routing_key
        )
        self.__fifo.put((payload, headers, routing_key))


class WazoEventMixin(BaseProtocol):
    '''
    Mixin to handle message formatting for wazo events

    Overrides:
        * `_marshal`:
            Serializes the message to be sent to RabbitMQ

        * `_unmarshal`:
            Deserializes the message received from RabbitMQ
    '''

    def __init__(self, service_uuid: str | None = None, **kwargs: Any):
        # NOTE(clanglois): Mixin expects a parent class to provide __init__ implementation
        super().__init__(**kwargs)  # type: ignore[safe-super]
        self.service_uuid = service_uuid

    def __generate_payload(
        self, event: EventProtocol, headers: dict, initial_data: dict | None
    ) -> dict:
        payload: dict = {}
        data = initial_data.copy() if initial_data else {}
        try:
            data.update(event.marshal())
        except AttributeError:
            self.log.exception("Received invalid event '%s'", event)
            raise ValueError('Not a valid Wazo Event')
        else:
            payload.update(headers, data=data)
            return payload

    def __generate_headers(
        self, event: EventProtocol, extra_headers: dict | None
    ) -> dict:
        headers = {}
        headers.update(extra_headers or {})

        try:
            headers.update(event.headers)
        except AttributeError:
            pass

        if hasattr(event, 'required_access'):
            headers['required_access'] = event.required_access

        # TODO: remove deprecated `required_acl`
        if hasattr(event, 'required_acl'):
            headers['required_acl'] = event.required_acl

        headers.update(
            name=event.name,
            origin_uuid=self.service_uuid,
            timestamp=datetime.now().isoformat(),
        )

        return headers

    def _marshal(
        self,
        event: EventProtocol,
        headers: dict | None,
        payload: dict | None,
        routing_key: str | None = None,
    ) -> tuple[dict, dict, str | None]:
        routing_key = routing_key or getattr(event, 'routing_key', None)
        headers = self.__generate_headers(event, headers)
        payload = self.__generate_payload(event, headers, payload)

        return headers, payload, routing_key

    def _unmarshal(
        self, event_name: str, headers: dict, payload: dict
    ) -> tuple[dict, dict]:
        if not isinstance(payload, dict):
            raise ValueError(
                f"Invalid payload for event '{event_name}': "
                f"expected dict, got {type(payload).__name__}"
            )
        event_data = payload.pop('data')
        headers = headers or payload
        return headers, event_data


class CollectdMixin:
    content_type: ClassVar[str] = 'text/collectd'

    def __init__(self, service_uuid: str | None = None, **kwargs: Any):
        super().__init__(**kwargs)
        if not service_uuid:
            raise ValueError('service must have an UUID')
        self.service_uuid = service_uuid

    def __generate_payload(self, event: CollectdEvent) -> str:
        if not event.is_valid():
            raise ValueError(event)

        host = self.service_uuid

        plugin = event.plugin
        if event.plugin_instance:
            plugin = f'{event.plugin}-{event.plugin_instance}'

        type_ = f'{event.type_}-{event.type_instance}'
        interval = event.interval
        time = event.time
        values = ':'.join(event.values)

        return f'PUTVAL {host}/{plugin}/{type_} interval={interval} {time}:{values}'

    def _marshal(
        self,
        event: CollectdEvent,
        headers: dict | None,
        payload: dict | None,
        routing_key: str | None = None,
    ) -> tuple[dict | None, str, str | None]:
        routing_key = routing_key or getattr(event, 'routing_key', None)
        collectd_payload: str = self.__generate_payload(event)

        return headers, collectd_payload, routing_key
