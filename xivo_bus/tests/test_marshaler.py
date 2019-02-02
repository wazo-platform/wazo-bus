# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import unittest

from hamcrest import assert_that
from hamcrest import calling
from hamcrest import equal_to
from hamcrest import instance_of
from hamcrest import raises
from mock import Mock

from xivo_bus.marshaler import CollectdMarshaler, Marshaler, InvalidMessage

SOME_UUID = '15924520-1b3b-4ee4-xivo-8ce47a1e6c01'


class EventTest(object):
    def __init__(self, value):
        self.value = value

    def marshal(self):
        return {'value': self.value}

    @classmethod
    def unmarshal(cls, message):
        return cls(message['value'])


class TestMarshaler(unittest.TestCase):

    def setUp(self):
        self.uuid = SOME_UUID
        self.marshaler = Marshaler(self.uuid)
        self.command = Mock()
        self.command.name = 'foobar'
        self.command.required_acl = 'some.acl'
        self.command.marshal.return_value = {'a': 1}
        self.expected = {'name': 'foobar',
                         'required_acl': 'some.acl',
                         'origin_uuid': self.uuid,
                         'data': {'a': 1}}

    def test_marshal_message(self):
        result = self.marshaler.marshal_message(self.command)

        assert_that(json.loads(result), equal_to(self.expected))

    def test_marshal_message_without_required_acl(self):
        del self.command.required_acl
        del self.expected['required_acl']

        result = self.marshaler.marshal_message(self.command)

        assert_that(json.loads(result), equal_to(self.expected))

    def test_marshal_message_with_none_required_acl(self):
        self.command.required_acl = None
        self.expected['required_acl'] = None

        result = self.marshaler.marshal_message(self.command)

        assert_that(json.loads(result), equal_to(self.expected))

    def test_given_invalid_message_when_unmarshal_message_then_raise(self):
        for invalid_message in ('asdlfkassdfsdfasdgas',
                                {},
                                {'data': None},
                                {'origin_uuid': None}):
            assert_that(calling(Marshaler.unmarshal_message).with_args(invalid_message, EventTest),
                        raises(InvalidMessage))

    def test_given_valid_message_when_unmarshal_message_then_return_object(self):
        message = {'data': {'value': 1234},
                   'origin_uuid': 'some-origin'}

        result = Marshaler.unmarshal_message(message, EventTest)

        assert_that(result, instance_of(EventTest))
        assert_that(result.value, equal_to(1234))
        assert_that(result.metadata, equal_to({'origin_uuid': 'some-origin'}))


class TestMarshalerCollectd(unittest.TestCase):

    def setUp(self):
        self.uuid = SOME_UUID
        self.marshaler = CollectdMarshaler(self.uuid)

    def test_marshal_invalid(self):
        command = Mock()
        command.is_valid.return_value = False

        assert_that(calling(self.marshaler.marshal_message).with_args(command), raises(ValueError))

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

        expected = 'PUTVAL {uuid}/my-plugin/mytype-myinstance interval=1 N:2:3'.format(uuid=self.uuid)

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

        expected = 'PUTVAL {uuid}/my-plugin/mytype-myinstance interval=1 42:2:3'.format(uuid=self.uuid)

        assert_that(result, equal_to(expected))
