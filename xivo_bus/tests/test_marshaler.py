# -*- coding: utf-8 -*-

# Copyright (C) 2012-2015 Avencall
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

import json
import unittest

from hamcrest import assert_that, equal_to
from mock import Mock

from xivo_bus.marshaler import Marshaler


class TestMarshaler(unittest.TestCase):

    def setUp(self):
        self.uuid = '15924520-1b3b-4ee4-xivo-8ce47a1e6c01'

    def test_marshal_message(self):
        command = Mock()
        command.name = 'foobar'
        command.marshal.return_value = {'a': 1}

        marshal = Marshaler(self.uuid)

        result = marshal.marshal_message(command)

        expected = {'name': 'foobar',
                    'origin_uuid': self.uuid,
                    'data': {'a': 1}}

        assert_that(json.loads(result), equal_to(expected))

    def test_unmarshal_message(self):
        json = '{"error": null, "value": "foobar"}'
        expected = {'value': 'foobar', 'error': None}
        marshal = Marshaler(self.uuid)

        result = marshal.unmarshal_message(json)

        self.assertEquals(result, expected)
