# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
import uuid

from hamcrest import assert_that, equal_to
from mock import sentinel as s

from ..event import ServiceRegisteredEvent, ServiceDeregisteredEvent


class TestServiceRegisteredEvent(unittest.TestCase):

    def test_marshal(self):
        service_name = 'wazo-calld'
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
        service_name = 'wazo-calld'
        service_id = str(uuid.uuid4())
        service_tags = ['tag1', 'tag2']

        event = ServiceDeregisteredEvent(service_name,
                                         service_id,
                                         service_tags)

        msg = event.marshal()

        assert_that(msg, equal_to({'service_name': service_name,
                                   'service_id': service_id,
                                   'tags': service_tags}))
