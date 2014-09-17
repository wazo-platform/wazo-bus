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

import logging
import pika

from xivo_bus.ctl.marshaler import Marshaler
from xivo_bus.ctl.config import BusConfig

logger = logging.getLogger(__name__)


class BusConsumerError(Exception):

    def __init__(self, error):
        Exception.__init__(self, error)
        self.error = error


class BusConsumer(object):

    def __init__(self, config=None):
        if not config:
            config = BusConfig()
        self._connection_params = config.to_connection_params()
        self._marshaler = Marshaler()

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(self._connection_params)
            self.channel = self.connection.channel()
        except pika.exceptions.AMQPConnectionError, e:
            raise BusConsumerError(e)

    def add_binding(self, callback, queue_name, exchange, key):
        self.callback = callback
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, exclusive=False, durable=True)
        try:
            self.channel.queue_bind(queue=queue_name, exchange=exchange, routing_key=key)
        except pika.exceptions.ChannelClosed, e:
            logger.error(e)

    def on_message(self, channel, method, header, body):
        body = self._marshaler.unmarshal_message(body)
        logger.debug('Received new event : %s', body)
        self.callback(body)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        try:
            self.channel.basic_consume(self.on_message, self.queue_name)
            self.channel.start_consuming()
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.ChannelClosed) as e:
            raise BusConsumerError(e)

    def stop(self):
        if self.connection.is_open:
            self.channel.stop_consuming()
            self.connection.close()
