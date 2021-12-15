# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_entry, empty, is_, has_item, has_items

from .helpers import BusIntegrationTest


class TestHeaders(BusIntegrationTest):
    asset = 'headers'

    def test_bind_unbind(self):
        event = 'binding_test'

        self.bus.bind(event)
        self.bus.publish(event, "first payload")

        self.bus.unbind(event)
        self.bus.publish(event, "second payload")

        assert_that(self.bus.get_messages(event), has_item("first payload"))

    def test_routing_key_disabled_with_headers_exchange(self):
        event = 'routing_key_event'
        key = 'events.good_key.#'

        with self.use_event(event, routing_key=key):
            self.bus.publish(event, "message1", routing_key='events.good_key.here')
            self.bus.publish(event, "message2", routing_key='events.wrong_key.here')

        assert_that(self.bus.get_messages(event), has_items("message1", "message2"))

    def test_bind_on_headers(self):
        event = 'bound_headers'
        headers = {'must_have': 'headers'}

        with self.use_event(event, headers=headers):
            self.bus.publish(event, {'some': 'payload'}, headers=headers)

        assert_that(
            self.bus.get_messages(event), has_item((has_entry('some', 'payload')))
        )

    def test_publish_without_expected_headers(self):
        event = 'no_publish_headers'
        headers = {'must_have': 'this'}

        with self.use_event(event, headers=headers):
            self.bus.publish(event, "payload")

        assert_that(self.bus.get_messages(event), is_(empty()))

    def test_publish_wrong_expected_headers_value(self):
        event = 'wrong_headers_value'
        headers = {'required': True}

        with self.use_event(event, headers=headers):
            self.bus.publish(event, "payload", headers={'required': False})

        assert_that(self.bus.get_messages(event), is_(empty()))

    def test_publish_ignore_extra_headers(self):
        event = 'extra_ignored_headers'
        headers = {'required': True}

        with self.use_event(event, headers=headers):
            self.bus.publish(
                event,
                {'some': 'payload'},
                headers={'required': True, 'other': 1, 'ignored': 'headers'},
            )

        assert_that(
            self.bus.get_messages(event), has_item((has_entry('some', 'payload')))
        )
