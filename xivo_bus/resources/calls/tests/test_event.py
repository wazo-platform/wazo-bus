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

from hamcrest import assert_that, equal_to

from ..event import CreateCallEvent


class TestCreateCallEvent(unittest.TestCase):

    def test_marshal(self):
        data = {
            'test': 'test'
        }

        event = CreateCallEvent(data)

        result = event.marshal()

        expected_payload = { 'data': {
                                  'test': 'test' }
                           }
        expected_routing_key = 'calls.call.created'

        assert_that(result, equal_to(expected_payload))
        assert_that(event.routing_key, equal_to(expected_routing_key))
