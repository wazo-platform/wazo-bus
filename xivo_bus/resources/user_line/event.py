# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserLineConfigEvent(ResourceConfigEvent):
    routing_key = 'config.user_line_association.{}'

    def __init__(self,
                 user_id,
                 line_id,
                 main_user,
                 main_line):
        self.user_id = int(user_id)
        self.line_id = int(line_id)
        self.main_user = bool(main_user)
        self.main_line = bool(main_line)

    def marshal(self):
        return {
            'user_id': self.user_id,
            'line_id': self.line_id,
            'main_user': self.main_user,
            'main_line': self.main_line
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_id'],
            msg['line_id'],
            msg['main_user'],
            msg['main_line'])


class UserLineAssociatedEvent(UserLineConfigEvent):
    name = 'line_associated'
    routing_key = UserLineConfigEvent.routing_key.format('created')


class UserLineDissociatedEvent(UserLineConfigEvent):
    name = 'line_dissociated'
    routing_key = UserLineConfigEvent.routing_key.format('deleted')
