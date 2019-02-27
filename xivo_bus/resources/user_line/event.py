# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseUserLineEvent(BaseEvent):

    def __init__(self, user, line, main_user, main_line):
        self._body = {
            'line': line,
            'main_line': main_line,
            'main_user': main_user,
            'user': user,
        }
        super(_BaseUserLineEvent, self).__init__()


class UserLineAssociatedEvent(_BaseUserLineEvent):

    name = 'user_line_associated'
    routing_key_fmt = 'config.users.{user[uuid]}.lines.{line[id]}.updated'


class UserLineDissociatedEvent(_BaseUserLineEvent):

    name = 'user_line_dissociated'
    routing_key_fmt = 'config.users.{user[uuid]}.lines.{line[id]}.deleted'
