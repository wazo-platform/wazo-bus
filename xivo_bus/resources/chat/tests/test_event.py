# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

import unittest
import uuid as uuid_

from hamcrest import assert_that, equal_to

from ..event import ChatMessageEvent


def uuid():
    return str(uuid_.uuid4())


class TestChatMessageEvent(unittest.TestCase):

    def test_marshal(self):
        user_1_id, user_2_id = 42, 5
        xivo_1_uuid, xivo_2_uuid = uuid(), uuid()
        destination = xivo_1_uuid, user_1_id
        origin = xivo_2_uuid, user_2_id
        alias = 'Alïce'
        msg = 'Salut, ça va?'

        event = ChatMessageEvent(origin, destination, alias, msg)
        marshalled_msg = event.marshal()

        expected_payload = {'from': origin,
                            'to': destination,
                            'alias': alias,
                            'msg': msg}
        expected_routing_key = 'chat.message.{uuid}.{id}'.format(uuid=xivo_1_uuid, id=user_1_id)
        assert_that(marshalled_msg, equal_to(expected_payload))
        assert_that(event.routing_key, equal_to(expected_routing_key))
