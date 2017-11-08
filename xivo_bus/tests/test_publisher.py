# -*- coding: utf-8 -*-

# Copyright 2015-2017 The Wazo Authors  (see the AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0+

import unittest

from mock import Mock, sentinel

from xivo_bus.marshaler import Marshaler
from xivo_bus.publisher import Publisher

SOME_HEADERS = {'header1': 'value1', 'override-me': 'value'}


class TestPublisher(unittest.TestCase):

    def setUp(self):
        self.publish = Mock()
        self.producer = Mock()
        self.producer.connection.ensure.return_value = self.publish
        self.marshaler = Mock(Marshaler)
        self.marshaler.marshal_message.return_value = sentinel.data
        self.publisher = Publisher(self.producer, self.marshaler)

    def test_publish(self):
        event = Mock()
        event.routing_key = 'foobar'
        self.marshaler.content_type = 'bazglop'
        self.marshaler.metadata.return_value = SOME_HEADERS

        self.publisher.publish(event)

        self.marshaler.marshal_message.assert_called_once_with(event)
        self.publish.assert_called_once_with(
            sentinel.data, routing_key='foobar', headers=SOME_HEADERS, content_type='bazglop')

    def test_publish_with_headers(self):
        event = Mock()
        event.routing_key = 'foobar'
        custom_headers = {'user_uuid': 'some-uuid', 'override-me': 'overridden'}
        expected_headers = {'header1': 'value1',
                            'user_uuid': 'some-uuid',
                            'override-me': 'overridden'}
        self.marshaler.content_type = 'bazglop'
        self.marshaler.metadata.return_value = SOME_HEADERS

        self.publisher.publish(event, custom_headers)

        self.marshaler.marshal_message.assert_called_once_with(event)
        self.publish.assert_called_once_with(
            sentinel.data, routing_key='foobar', headers=expected_headers, content_type='bazglop')
