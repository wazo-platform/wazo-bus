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

import unittest

from mock import Mock
from xivo_bus.ctl.marshaler import Marshaler, CommandResponse


class TestMarshaler(unittest.TestCase):

    def test_marshal_command(self):
        command = Mock()
        command.name = 'foobar'
        command.marshal.return_value = {'a': 1}

        marshal = Marshaler()

        result = marshal.marshal_command(command)

        command.marshal.assert_called_once_with()
        self.assertEquals(result, ('{"data": {"a": 1}, "name": "foobar"}'))

    def test_unmarshal_response(self):
        json = '{"error": null, "value": "foobar"}'

        marshal = Marshaler()
        result = marshal.unmarshal_response(json)

        self.assertTrue(isinstance(result, CommandResponse))
        self.assertEquals(result.value, 'foobar')
        self.assertEquals(result.error, None)

    def test_unmarshal_message(self):
        json = '{"error": null, "value": "foobar"}'
        expected = {'value': 'foobar', 'error': None}
        marshal = Marshaler()

        result = marshal.unmarshal_message(json)

        self.assertEquals(result, expected)
