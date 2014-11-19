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
from ..event import UserFuncKeyEvent, BSFilterFuncKeyEvent

ID = 1
USER_ID = 2
FILTER_ID = 3
SECRETARY_ID = 4


class ConcreteUserFuncKeyEvent(UserFuncKeyEvent):
    name = 'user_func_key'


class ConcreteBSFilterFuncKeyEvent(BSFilterFuncKeyEvent):
    name = 'bsfilter_func_key'


class TestAbstractUserFuncKeyEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
            'destination': 'user',
            'user_id': USER_ID,
        }

    def test_marshal(self):
        command = ConcreteUserFuncKeyEvent(ID, USER_ID)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteUserFuncKeyEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteUserFuncKeyEvent.name)
        self.assertEqual(command.func_key_id, ID)
        self.assertEqual(command.user_id, USER_ID)


class TestAbstractBSFilterFuncKeyEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
            'destination': 'bsfilter',
            'secretary_id': SECRETARY_ID,
            'filter_id': FILTER_ID,
        }

    def test_marshal(self):
        command = ConcreteBSFilterFuncKeyEvent(ID, FILTER_ID, SECRETARY_ID)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteBSFilterFuncKeyEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteBSFilterFuncKeyEvent.name)
        self.assertEqual(command.func_key_id, ID)
        self.assertEqual(command.filter_id, FILTER_ID)
        self.assertEqual(command.secretary_id, SECRETARY_ID)
