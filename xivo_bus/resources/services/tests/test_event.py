# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
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
import uuid

from ..event import ServiceRegisteredEvent, ServiceDeregisteredEvent

from hamcrest import assert_that, equal_to
from mock import sentinel as s


class TestServiceRegisteredEvent(unittest.TestCase):

    def test_marshal(self):
        service_name = 'xivo-ctid'
        service_id = str(uuid.uuid4())
        service_tags = ['tag1', 'tag2']

        event = ServiceRegisteredEvent(service_name,
                                       service_id,
                                       s.address,
                                       s.port,
                                       service_tags)

        msg = event.marshal()

        assert_that(msg, equal_to({'service_name': service_name,
                                   'service_id': service_id,
                                   'address': s.address,
                                   'port': s.port,
                                   'tags': service_tags}))


class TestServiceDeregisteredEvent(unittest.TestCase):

    def test_marshal(self):
        service_name = 'xivo-ctid'
        service_id = str(uuid.uuid4())
        service_tags = ['tag1', 'tag2']

        event = ServiceDeregisteredEvent(service_name,
                                         service_id,
                                         service_tags)

        msg = event.marshal()

        assert_that(msg, equal_to({'service_name': service_name,
                                   'service_id': service_id,
                                   'tags': service_tags}))
