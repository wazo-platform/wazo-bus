# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


import unittest
from unittest.mock import sentinel

from ..event import AMIEvent


class TestAMIEvent(unittest.TestCase):
    def test_marshal(self):
        event = AMIEvent(sentinel.name, {'vars': sentinel.variables})

        result = event.marshal()

        self.assertEqual(result, {'vars': sentinel.variables})

    def test_string_name(self):
        sentinel.name = 'some-ami-event'
        event = AMIEvent(sentinel.name, {'vars': sentinel.variables})

        self.assertEqual(event.name, sentinel.name)
