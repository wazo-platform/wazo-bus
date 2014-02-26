# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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
from ..event import FuncKeyConfigEvent

ID = 1
TYPE = 'speeddial'
DESTINATION = 'user'
DESTINATION_ID = 2


class ConcreteFuncKeyConfigEvent(FuncKeyConfigEvent):

    name = 'func_key'


class TestAbstractFuncKeyConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
            'type': TYPE,
            'destination': DESTINATION,
            'destination_id': DESTINATION_ID,
        }

    def test_marshal(self):
        command = ConcreteFuncKeyConfigEvent(ID, TYPE, DESTINATION, DESTINATION_ID)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteFuncKeyConfigEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteFuncKeyConfigEvent.name)
        self.assertEqual(command.id, ID)
        self.assertEqual(command.type, TYPE)
        self.assertEqual(command.destination, DESTINATION)
        self.assertEqual(command.destination_id, DESTINATION_ID)
