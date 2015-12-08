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
