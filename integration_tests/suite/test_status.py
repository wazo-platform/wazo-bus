# Copyright 2022-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, calling, raises, has_item, has_entry
from wazo_test_helpers import until
from kombu.exceptions import OperationalError

from .helpers.base import BusIntegrationTest
from .helpers.events import MockEvent


class TestStatus(BusIntegrationTest):
    asset = 'headers'

    def check_is_running(self):
        remote_status = self.remote_bus.get_status()
        return self.local_bus.is_running and remote_status['running']

    def test_status_when_all_ok(self):
        until.true(self.check_is_running, tries=3)

    def test_status_when_rabbitmq_restarts(self):
        self.stop_rabbitmq()
        until.false(self.check_is_running, timeout=30)
        self.start_rabbitmq()
        until.true(self.check_is_running, timeout=30)

    def test_status_when_service_restart(self):
        self.reset_clients()
        until.true(self.check_is_running, tries=3)

    def test_publish_timeout_when_rabbitmq_is_down_then_up(self):
        event = MockEvent('some_event', value='some_value')

        self.stop_rabbitmq()

        with self.local_event(event.name):
            assert_that(
                calling(self.local_bus.publish).with_args(event),
                raises(OperationalError),
            )

            self.start_rabbitmq()
            until.true(self.check_is_running, timeout=30)

            self.local_bus.publish(event)
            assert_that(
                self.local_messages(event.name, 1),
                has_item(has_entry('value', 'some_value')),
            )
