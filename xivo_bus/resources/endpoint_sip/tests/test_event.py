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

from __future__ import unicode_literals

import unittest
from ..event import SipEndpointConfigEvent

ID = 42


class ConcreteSipEndpointConfigEvent(SipEndpointConfigEvent):

    name = 'foo'


class TestAbstractSipEndpointIDParams(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
        }

    def test_marshal(self):
        command = ConcreteSipEndpointConfigEvent(ID)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteSipEndpointConfigEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteSipEndpointConfigEvent.name)
        self.assertEqual(command.id, ID)
