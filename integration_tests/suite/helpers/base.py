# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from inspect import isclass
import os
from time import sleep
from contextlib import contextmanager
from hamcrest import assert_that, is_, is_in

from wazo_test_helpers.asset_launching_test_case import AssetLaunchingTestCase

from .busclient import BusApiClient
from .accumulator import MessageAccumulator
from xivo_bus.base import BusConnector


class BusIntegrationTest(AssetLaunchingTestCase):
    assets_root = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
    service = 'xivo-bus'
    EXCHANGE_NAME = 'bus-integration-tests'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.local_bus = BusConnector(
            exchange_name=cls.EXCHANGE_NAME, exchange_type=cls.asset
        )
        cls.local_bus.start()
        cls._local_messages = MessageAccumulator()
        cls.remote_bus = BusApiClient(host='localhost', port=6444)
        sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.local_bus.stop()
        super().tearDownClass()

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
            sleep(0.05)  # Allow bindings to be installed on server
            yield
        except Exception:
            raise
        finally:
            sleep(0.05)  # Allow consumers to consume all messages
            assert_that(cls.local_bus.unsubscribe(event, handler), is_(True))

    @classmethod
    def local_messages(cls, event):
        return cls._local_messages.pop(event)

    @classmethod
    def remote_messages(cls, event):
        return cls.remote_bus.get_messages(event)

    @classmethod
    @contextmanager
    def remote_middleware(cls, middleware, *args, **kwargs):
        try:
            assert_that(
                cls.remote_bus.register_middleware(middleware, *args, **kwargs),
                is_(True),
            )
            yield
        except AssertionError:
            raise
        finally:
            assert_that(cls.remote_bus.unregister_middleware(middleware), is_(True))

    @classmethod
    @contextmanager
    def local_middleware(cls, middleware, *args, **kwargs):
        if isclass(middleware):
            middleware = middleware(*args, **kwargs)

        try:
            cls.local_bus.register_middleware(middleware)
            assert_that(middleware, is_in(cls.local_bus._MiddlewareMixin__middlewares))
            yield
        except Exception:
            raise
        finally:
            cls.local_bus.unregister_middleware(middleware)
