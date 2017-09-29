# -*- coding: utf-8 -*-

# Copyright 2015-2017 The Wazo Authors  (see the AUTHORS file)
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


class BaseChatMessageEvent(object):

    def __init__(self, from_, to, alias, msg):
        self.required_acl = 'events.{}'.format(self.routing_key)
        self._from = from_
        self._to = to
        self._alias = alias
        self._msg = msg

    def marshal(self):
        return {'from': self._from,
                'to': self._to,
                'alias': self._alias,
                'msg': self._msg}

    def __eq__(self, other):
        return (self._from == other._from and
                self._to == other._to and
                self._alias == other._alias and
                self._msg == other._msg)

    def __ne__(self, other):
        return not self.__eq__(other)


class ChatMessageEvent(BaseChatMessageEvent):

    name = 'chat_message_event'
    routing_key_fmt = 'chat.message.{}.{}'

    def __init__(self, from_, to, alias, msg):
        self.routing_key = self.routing_key_fmt.format(*to)
        super(ChatMessageEvent, self).__init__(from_, to, alias, msg)


class ChatMessageReceived(BaseChatMessageEvent):

    name = 'chat_message_received'
    routing_key_fmt = 'chat.message.{}.{}.received'

    def __init__(self, from_, to, alias, msg):
        self.routing_key = self.routing_key_fmt.format(*to)
        super(ChatMessageReceived, self).__init__(from_, to, alias, msg)


class ChatMessageSent(BaseChatMessageEvent):

    name = 'chat_message_sent'
    routing_key_fmt = 'chat.message.{}.{}.sent'

    def __init__(self, from_, to, alias, msg):
        self.routing_key = self.routing_key_fmt.format(*from_)
        super(ChatMessageSent, self).__init__(from_, to, alias, msg)
