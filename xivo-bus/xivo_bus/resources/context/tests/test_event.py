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
from ..event import ContextConfigEvent


class ConcreteContextConfigEvent(ContextConfigEvent):

    name = 'foo'


ID = 1
NAME = 'foo_context'
DISPLAY_NAME = 'Foo Context'
DESCRIPTION = 'description'
TYPE = 'internal'


class TestAbstractContextConfigEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
            'name': NAME,
            'display_name': DISPLAY_NAME,
            'description': DESCRIPTION,
            'type': TYPE
        }

    def test_marshal(self):
        command = ConcreteContextConfigEvent(ID, NAME, DISPLAY_NAME, DESCRIPTION, TYPE)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteContextConfigEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteContextConfigEvent.name)
        self.assertEqual(command.id, ID)
        self.assertEqual(command.context_name, NAME)
        self.assertEqual(command.display_name, DISPLAY_NAME)
        self.assertEqual(command.description, DESCRIPTION)
        self.assertEqual(command.context_type, TYPE)
