# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from time import sleep
from contextlib import contextmanager
from hamcrest import assert_that, is_

from wazo_test_helpers.asset_launching_test_case import (
    AssetLaunchingTestCase,
    NoSuchService,
)
from xivo_bus.base import Base
from xivo_bus.mixins import (
    ThreadableMixin,
    ConsumerMixin,
    QueuePublisherMixin,
    WazoEventMixin,
)
from .remote_bus import RemoteBusApiClient
from .accumulator import MessageAccumulator


class Bus(ThreadableMixin, ConsumerMixin, QueuePublisherMixin, Base):
    pass


class WazoBus(WazoEventMixin, Bus):
    pass


class BusIntegrationTest(AssetLaunchingTestCase):
    assets_root = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
    service = 'bus'
    _local_messages = MessageAccumulator()

    EXCHANGE_NAME = 'bus-integration-tests'
    TEST_WAZO_EVENTS = False

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
        cls.local_bus = cls.make_local_bus()
        cls.remote_bus = cls.make_remote_bus()
        cls.local_bus.start()

    @classmethod
    def make_local_bus(cls):
        try:
            port = cls.service_port(5672, 'rabbitmq')
        except NoSuchService:
            return
        bus_cls = WazoBus if cls.TEST_WAZO_EVENTS else Bus
        return bus_cls(
            name='local-bus',
            service_uuid='00000000-0000-0000-0000-000000000001',
            host='127.0.0.1',
            port=port,
            exchange_name=cls.EXCHANGE_NAME,
            exchange_type=cls.asset,
        )

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
                cls.remote_bus.subscribe(
                    event, headers=headers, routing_key=routing_key
                ),
                is_(True),
            )
            yield
        except AssertionError:
            raise
        finally:
            assert_that(
                cls.remote_bus.unsubscribe(
                    event, headers=headers, routing_key=routing_key
                ),
                is_(True),
            )

    @classmethod
    @contextmanager
    def local_event(cls, event, headers=None, routing_key=None):
        handler = cls._local_messages.create_handler(event)
        headers = headers or {}
        headers.setdefault('name', event)
        try:
            cls.local_bus.subscribe(
                event, handler, headers=headers, routing_key=routing_key
            )
            sleep(0.01)  # Allow bindings to be installed on server
            yield
        except Exception:
            raise
        finally:
            sleep(0.01)  # Allow consumers to consume all messages
            assert_that(cls.local_bus.unsubscribe(event, handler), is_(True))

    @classmethod
    def local_messages(cls, event):
        return cls._local_messages.pop(event)

    @classmethod
    def remote_messages(cls, event):
        return cls.remote_bus.get_messages(event)
