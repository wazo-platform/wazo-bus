# -*- coding: utf-8 -*-

# Copyright 2015-2017 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

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
