# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
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

from mock import Mock, patch
import unittest
from xivo_bus.ctl.consumer import BusConsumer

QUEUE_NAME = 'xivo-call-logd-queue'


class TestBusConsumer(unittest.TestCase):

    def setUp(self):
        self.consumer = BusConsumer()
        self.consumer.channel = Mock()
        self.callback = Mock()

    @patch('pika.BlockingConnection')
    @patch('pika.ConnectionParameters')
    def test_when_connect_then_instantiate_connection_and_channel(self, parameters_mock, connection_mock):
        parameters = parameters_mock('localhost')

        self.consumer.connect()

        connection_mock.assert_called_once_with(parameters)

    def test_when_add_binding_then_channel_queue_bind(self):
        exchange = 'xivo-ami'
        key = '*'

        self.consumer.add_binding(self.callback, QUEUE_NAME, exchange, key)

        self.consumer.channel.queue_declare.assert_called_once_with(queue=QUEUE_NAME, exclusive=False, durable=True)
        self.consumer.channel.queue_bind.assert_called_once_with(
            queue=QUEUE_NAME, exchange=exchange, routing_key=key)

    def test_when_run_then_consume(self):
        self.consumer.callback = self.callback
        self.consumer.queue_name = QUEUE_NAME

        self.consumer.run()

        self.consumer.channel.basic_consume.assert_called_once_with(self.callback, QUEUE_NAME)
        self.consumer.channel.start_consuming.assert_called_once_with()

    @patch('pika.BlockingConnection')
    @patch('pika.ConnectionParameters')
    def test_when_stop_then_stop_and_disconnect(self, parameters_mock, connection_mock):
        self.consumer.connect()
        self.consumer.stop()

        self.consumer.channel.stop_consuming.assert_called_once_with()
        self.consumer.connection.close.assert_called_once_with()
        self.consumer.connection.disconnect.assert_called_once_with()
