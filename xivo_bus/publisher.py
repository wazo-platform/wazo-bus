# -*- coding: utf-8 -*-

# Copyright 2012-2017 The Wazo Authors  (see the AUTHORS file)
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

logger = logging.getLogger(__name__)


class Publisher(object):

    def __init__(self, producer, marshaler):
        self._publish = self._new_publish(producer)
        self._marshaler = marshaler

    def _new_publish(self, producer):
        conn = producer.connection
        return conn.ensure(producer, producer.publish,
                           errback=self._on_publish_error,
                           max_retries=2,
                           interval_start=1)

    def _on_publish_error(self, exc, interval):
        logger.error('Error: %s', exc, exc_info=1)
        logger.info('Retry in %s seconds...', interval)

    def publish(self, event, headers=None):
        data = self._marshaler.marshal_message(event)
        all_headers = dict(self._marshaler.metadata(event))
        all_headers.update(headers or {})
        self._publish(data,
                      content_type=self._marshaler.content_type,
                      routing_key=event.routing_key,
                      headers=all_headers)
