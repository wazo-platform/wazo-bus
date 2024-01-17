# Copyright 2021-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from contextlib import contextmanager
from uuid import uuid4

from hamcrest import assert_that, is_
from wazo_test_helpers import until
from wazo_test_helpers.asset_launching_test_case import (
    AssetLaunchingTestCase,
    NoSuchService,
)

from wazo_bus.consumer import BusConsumer
from wazo_bus.publisher import BusPublisherWithQueue

from .accumulator import MessageAccumulator
from .remote_bus import RemoteBusApiClient
from .wait_strategies import wait_for_rabbitmq


class Bus(BusConsumer, BusPublisherWithQueue):
    pass


class BusIntegrationTest(AssetLaunchingTestCase):
    assets_root = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
    service = 'bus'
    EXCHANGE_NAME = 'bus-integration-tests'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reset_clients()

    @classmethod
    def tearDownClass(cls):
        cls.local_bus.stop()
        super().tearDownClass()

    @classmethod
    def reset_clients(cls):
        cls._local_messages = MessageAccumulator()
        cls.local_bus = cls.make_local_bus()
        cls.remote_bus = cls.make_remote_bus()

    @classmethod
    def stop_rabbitmq(cls):
        cls.stop_service('rabbitmq')

    @classmethod
    def start_rabbitmq(cls):
        cls.start_service('rabbitmq')
        port = cls.service_port(5672, 'rabbitmq')
        # Note: only needed on integration tests because ports are dynamic
        url = f'amqp://guest:guest@127.0.0.1:{port}//'
        cls.local_bus._PublisherMixin__connection.switch(url)
        cls.local_bus._ConsumerMixin__connection.switch(url)
        cls.local_bus.connection.switch(url)
        wait_for_rabbitmq(cls)

    @classmethod
    def make_local_bus(cls):
        if hasattr(cls, 'local_bus'):
            cls.local_bus.stop()

        try:
            port = cls.service_port(5672, 'rabbitmq')
        except NoSuchService:
            return
        bus = Bus(
            name='local-bus',
            service_uuid=str(uuid4()),
            host='127.0.0.1',
            port=port,
            exchange_name=cls.EXCHANGE_NAME,
            exchange_type=cls.asset,
        )
        bus.start()
        return bus

    @classmethod
    def make_remote_bus(cls):
        try:
            port = cls.service_port(5000, 'bus')
        except NoSuchService:
            return
        return RemoteBusApiClient(host='localhost', port=port)

    @classmethod
    @contextmanager
    def remote_event(cls, event, headers=None, routing_key=None):
        try:
            assert_that(
                cls.remote_bus.subscribe(event, headers, routing_key=routing_key),
                is_(True),
            )
            yield
        except Exception:
            raise
        finally:
            assert_that(
                cls.remote_bus.unsubscribe(event, headers, routing_key=routing_key),
                is_(True),
            )

    @classmethod
    @contextmanager
    def local_event(cls, event, headers=None, routing_key=None):
        handler = cls._local_messages.create_handler(event)
        try:
            cls.local_bus.subscribe(event, handler, headers, routing_key)
            yield
        except Exception:
            raise
        finally:
            assert_that(cls.local_bus.unsubscribe(event, handler), is_(True))

    @classmethod
    def local_messages(cls, event_name, expected=None, timeout=3.0):
        def test():
            return cls._local_messages.count(event_name) == expected

        try:
            until.true(test, timeout=timeout, interval=0.1)
        except until.NoMoreTries:
            pass
        return cls._local_messages.pop(event_name)

    @classmethod
    def remote_messages(cls, event_name, expected=None, timeout=3.0):
        def test():
            return cls.remote_bus.get_messages_count == expected

        try:
            until.true(test, timeout=timeout, interval=0.1)
        except until.NoMoreTries:
            pass
        return cls.remote_bus.get_messages(event_name)
