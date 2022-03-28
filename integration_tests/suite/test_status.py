# Copyright 2022-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_test_helpers import until
from .helpers.base import BusIntegrationTest


class TestStatus(BusIntegrationTest):
    asset = 'headers'

    def check_is_running(self):
        remote_status = self.remote_bus.get_status()
        return self.local_bus.is_running and remote_status['running']

    def test_status_when_all_ok(self):
        until.true(self.check_is_running, tries=3)

    def test_reconnect_when_rabbitmq_restarts(self):
        self.stop_rabbitmq()
        until.false(self.check_is_running, timeout=30)
        self.start_rabbitmq()
        until.true(self.check_is_running, timeout=30)

    def test_reconnect_when_service_restart(self):
        self.reset_clients()
        until.true(self.check_is_running, tries=3)
