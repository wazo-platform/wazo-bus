# -*- coding: utf-8 -*-
# Copyright (C) 2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

import unittest
from ..event import UserFuncKeyEvent, BSFilterFuncKeyEvent, FuncKeyTemplateEvent

ID = 1
USER_ID = 2
FILTER_ID = 3
SECRETARY_ID = 4


class ConcreteUserFuncKeyEvent(UserFuncKeyEvent):
    name = 'user_func_key'


class ConcreteBSFilterFuncKeyEvent(BSFilterFuncKeyEvent):
    name = 'bsfilter_func_key'


class ConcreteFuncKeyTemplateEvent(FuncKeyTemplateEvent):
    name = 'func_key_template'


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


class TestAbstractFuncKeyTemplateEvent(unittest.TestCase):

    def setUp(self):
        self.msg = {
            'id': ID,
        }

    def test_marshal(self):
        command = ConcreteFuncKeyTemplateEvent(ID)

        msg = command.marshal()

        self.assertEqual(msg, self.msg)

    def test_unmarshal(self):
        command = ConcreteFuncKeyTemplateEvent.unmarshal(self.msg)

        self.assertEqual(command.name, ConcreteFuncKeyTemplateEvent.name)
        self.assertEqual(command.id, ID)
