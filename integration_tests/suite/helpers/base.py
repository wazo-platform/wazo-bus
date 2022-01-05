# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from contextlib import contextmanager
from hamcrest import assert_that, is_

from wazo_test_helpers.asset_launching_test_case import AssetLaunchingTestCase
from .busclient import BusApiClient


class BusIntegrationTest(AssetLaunchingTestCase):
    assets_root = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
    service = 'xivo-bus'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bus = BusApiClient(host='localhost', port=6444)

    @classmethod
    @contextmanager
    def use_event(cls, event, headers=None, routing_key=None):
        try:
            assert_that(
                cls.bus.bind(event, headers=headers, routing_key=routing_key), is_(True)
            )
            yield
        except AssertionError:
            raise
        finally:
            assert_that(
                cls.bus.unbind(event, headers=headers, routing_key=routing_key),
                is_(True),
            )

    @classmethod
    @contextmanager
    def use_middleware(cls, bus_type, middleware, *args, **kwargs):
        try:
            assert_that(
                cls.bus.add_middleware(bus_type, middleware, *args, **kwargs),
                is_(True),
            )
            yield
        except AssertionError:
            raise
        finally:
            assert_that(cls.bus.remove_middleware(bus_type, middleware), is_(True))
