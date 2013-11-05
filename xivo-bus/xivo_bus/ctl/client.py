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

from xivo_bus.ctl.amqp_transport_client import AMQPTransportClient
from xivo_bus.ctl.marshaler import Marshaler
from xivo_bus.ctl.exception import BusCtlClientError


class BusCtlClient(object):

    _QUEUE_NAME = 'xivo'

    def __init__(self, fetch_response=True):
        self._fetch_response = fetch_response
        self._transport = None
        self._marshaler = Marshaler()

    def close(self):
        if self._transport is None:
            return

        self._transport.close()
        self._transport = None

    def connect(self):
        if self._transport is not None:
            raise Exception('already connected')

        self._transport = self._new_transport()

    def _new_transport(self):
        return AMQPTransportClient.create_and_connect(self._QUEUE_NAME)

    def _execute_command(self, cmd):
        request = self._marshaler.marshal_command(cmd)
        if self._fetch_response:
            return self._execute_request_fetch_response(request)
        else:
            return self._execute_request_no_fetch_response(request)

    def _execute_request_fetch_response(self, request):
        raw_response = self._transport.rpc_call(request)
        response = self._marshaler.unmarshal_response(raw_response)
        if response.error is not None:
            raise BusCtlClientError(response.error)
        return response.value

    def _execute_request_no_fetch_response(self, request):
        self._transport.send(request)
