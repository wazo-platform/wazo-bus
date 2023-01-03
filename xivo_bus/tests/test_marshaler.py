# Copyright 2012-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from hamcrest import assert_that
from hamcrest import calling
from hamcrest import equal_to
from hamcrest import raises
from mock import Mock
from xivo_bus.marshaler import CollectdMarshaler

SOME_UUID = '15924520-1b3b-4ee4-xivo-8ce47a1e6c01'


class EventTest:
    def __init__(self, value):
        self.value = value

    def marshal(self):
        return {'value': self.value}

    @classmethod
    def unmarshal(cls, message):
        return cls(message['value'])


class TestMarshalerCollectd(unittest.TestCase):
    def setUp(self):
        self.uuid = SOME_UUID
        self.marshaler = CollectdMarshaler(self.uuid)

    def test_marshal_invalid(self):
        command = Mock()
        command.is_valid.return_value = False

        assert_that(
            calling(self.marshaler.marshal_message).with_args(command),
            raises(ValueError),
        )

    def test_marshal_valid(self):
        command = Mock()
        command.is_valid.return_value = True
        command.plugin = 'my'
        command.plugin_instance = 'plugin'
        command.type_ = 'mytype'
        command.type_instance = 'myinstance'
        command.interval = '1'
        command.values = ('2', '3')
        command.time = 'N'

        result = self.marshaler.marshal_message(command)

        expected = 'PUTVAL {uuid}/my-plugin/mytype-myinstance interval=1 N:2:3'.format(
            uuid=self.uuid
        )

        assert_that(result, equal_to(expected))

    def test_marshal_valid_with_time(self):
        command = Mock()
        command.is_valid.return_value = True
        command.plugin = 'my'
        command.plugin_instance = 'plugin'
        command.type_ = 'mytype'
        command.type_instance = 'myinstance'
        command.interval = '1'
        command.values = ('2', '3')
        command.time = 42

        result = self.marshaler.marshal_message(command)

        expected = 'PUTVAL {uuid}/my-plugin/mytype-myinstance interval=1 42:2:3'.format(
            uuid=self.uuid
        )

        assert_that(result, equal_to(expected))
