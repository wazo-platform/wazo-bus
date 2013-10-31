# -*- coding: utf-8 -*-

# Copyright (C) 2012-2013 Avencall
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
from mock import Mock, patch, ANY
from xivo_bus.ctl.marshaler import Marshaler
from xivo_bus.ctl.amqp_transport_client import AMQPTransportClient
from xivo_bus.ctl.client import BusCtlClient


class TestBusCtlClient(unittest.TestCase):

    def setUp(self):
        self.marshaler = Mock(Marshaler)
        self.transport = Mock(AMQPTransportClient)
        self.bus_ctl_client = BusCtlClient()
        self.bus_ctl_client._marshaler = self.marshaler
        self.bus_ctl_client._transport = self.transport

    @patch('xivo_bus.ctl.client.AMQPTransportClient')
    def test_connect_no_transport(self, amqp_client_constructor):
        hostname = 'localhost'
        port = 5672

        client = BusCtlClient()
        client.connect(hostname, port)
        amqp_client_constructor.create_and_connect.assert_called_once_with(hostname, port, self.bus_ctl_client._QUEUE_NAME)

    @patch('xivo_bus.ctl.client.AMQPTransportClient', Mock())
    def test_connect_already_connected(self):
        hostname = 'localhost'
        port = 5672

        client = BusCtlClient()
        client.connect(hostname, port)
        self.assertRaises(Exception, client.connect, hostname, port)

    @patch('xivo_bus.ctl.client.AMQPTransportClient')
    def test_close_transport_with_no_connection(self, amqp_client):
        client = BusCtlClient()
        client.close()
        self.assertFalse(amqp_client.create_and_connect.called)

    @patch('xivo_bus.ctl.client.AMQPTransportClient')
    def test_connect_and_close_opens_and_closes_transport(self, amqp_client):
        transport = Mock()
        amqp_client.create_and_connect.return_value = transport

        client = BusCtlClient()
        client.connect()
        client.close()

        amqp_client.create_and_connect.assert_called_once_with(ANY, ANY, ANY)
        transport.close.assert_called_once_with()

    def test_execute_command_with_fetch_response(self):
        command = Mock()
        request = Mock()
        raw_response = Mock()
        response = Mock()
        response.error = None
        self.marshaler.marshal_command.return_value = request
        self.transport.rpc_call.return_value = raw_response
        self.marshaler.unmarshal_response.return_value = response

        self.bus_ctl_client._fetch_response = True
        result = self.bus_ctl_client._execute_command(command)

        self.marshaler.marshal_command.assert_called_once_with(command)
        self.transport.rpc_call.assert_called_once_with(request)
        self.assertEqual(result, response.value)

    def test_execute_command_without_fetch_response(self):
        command = Mock()
        request = Mock()
        self.marshaler.marshal_command.return_value = request

        self.bus_ctl_client._fetch_response = False
        self.bus_ctl_client._execute_command(command)

        self.marshaler.marshal_command.assert_called_once_with(command)
        self.transport.send.assert_called_once_with(request)

    @patch('xivo_bus.resources.xivo.command.PingCommand')
    def test_ping(self, PingCommand):
        command = Mock()

        PingCommand.return_value = command
        self.bus_ctl_client._execute_command = Mock()

        self.bus_ctl_client.ping()

        PingCommand.assert_called_once_with()
        self.bus_ctl_client._execute_command.assert_called_once_with(command)
