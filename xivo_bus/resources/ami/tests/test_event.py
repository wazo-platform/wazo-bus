# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


import unittest
from mock import sentinel
from ..event import AMIEvent


class TestAMIEvent(unittest.TestCase):
    def test_marshal(self):
        event = AMIEvent(sentinel.name, sentinel.variables)

        result = event.marshal()

        self.assertEqual(result, sentinel.variables)

    def test_string_name(self):
        sentinel.name = 'some-ami-event'
        event = AMIEvent(sentinel.name, sentinel.variables)

        self.assertEqual(event.name, sentinel.name)
