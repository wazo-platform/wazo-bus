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

from hamcrest import assert_that, equal_to
from mock import Mock, patch, sentinel
import unittest
from pika.exceptions import AMQPConnectionError
from pika.spec import Basic
from xivo_bus.ctl.consumer import BusConsumer, BusConnectionError
from xivo_bus.ctl.config import BusConfig

QUEUE_NAME = 'xivo-call-logd-queue'


class TestBusConsumer(unittest.TestCase):

    def setUp(self):
        self.config = Mock(BusConfig)
        self.config.to_connection_params.return_value = 'config'
        self.consumer_with_config = BusConsumer(self.config)
        self.consumer = BusConsumer()
        self.consumer.channel = Mock()
        self.callback = Mock()

        self.config.to_connection_params.assert_called_once_with()

    @patch('pika.BlockingConnection')
    def test_when_connect_then_instantiate_connection_and_channel_with_config(self, connection_mock):
        self.consumer_with_config.connect()

        self.config.to_connection_params.assert_called_once_with()
        connection_mock.assert_called_once_with('config')

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

        self.consumer.channel.basic_consume.assert_called_once_with(
            self.consumer.on_message, QUEUE_NAME)
        self.consumer.channel.start_consuming.assert_called_once_with()

    def test_rabbitmq_down_when_run_then_raise_busconnectionerror(self):
        self.consumer.channel.start_consuming.side_effect = [AMQPConnectionError()]
        self.consumer.callback = self.callback
        self.consumer.queue_name = QUEUE_NAME

        self.assertRaises(BusConnectionError, self.consumer.run)

    @patch('pika.BlockingConnection', Mock())
    @patch('pika.ConnectionParameters', Mock())
    def test_when_stop_then_stop_and_disconnect(self):
        self.consumer.connect()
        self.consumer.stop()

        self.consumer.channel.stop_consuming.assert_called_once_with()
        self.consumer.connection.close.assert_called_once_with()
        self.consumer.connection.close.assert_called_once_with()

    @patch('pika.BlockingConnection', Mock())
    @patch('pika.ConnectionParameters', Mock())
    def test_rabbitmq_down_when_stop_then_only_disconnect(self):
        self.consumer.connect()
        self.consumer.connection.is_open = False

        self.consumer.stop()

        assert_that(self.consumer.channel.stop_consuming.call_count, equal_to(0))
        assert_that(self.consumer.connection.close.call_count, equal_to(0))

    def test_when_on_message_then_unmarshal_callback_and_ack(self):
        channel = self.consumer.channel
        method = Mock(Basic.Deliver)
        method.delivery_tag = sentinel.tag
        linkedid = '1391789340.26'
        body = """
            {
            "data": {
                "EventTime": "2014-02-07 11:09:03",
                "LinkedID": "%s",
                "UniqueID": "1391789340.26",
                "EventName": "LINKEDID_END"
            },
            "name": "CEL"
            }
        """ % linkedid

        unmarshaled_body = {u'data':
                            {u'EventName': u'LINKEDID_END',
                             u'EventTime': u'2014-02-07 11:09:03',
                             u'LinkedID': u'1391789340.26',
                             u'UniqueID': u'1391789340.26'},
                            u'name': u'CEL'}

        self.consumer.callback = Mock()

        self.consumer.on_message(channel, method, sentinel.header, body)

        self.consumer.callback.assert_called_once_with(unmarshaled_body)
        channel.basic_ack.assert_called_once_with(delivery_tag=method.delivery_tag)
