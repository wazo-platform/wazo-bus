# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserLineExtensionConfigEvent(ResourceConfigEvent):

    def __init__(self,
                 user_line_extension_id,
                 user_id,
                 line_id,
                 extension_id,
                 main_user,
                 main_line):
        self.id = int(user_line_extension_id)
        self.user_id = int(user_id)
        self.line_id = int(line_id)
        self.extension_id = int(extension_id)
        self.main_user = bool(main_user)
        self.main_line = bool(main_line)

    def marshal(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'line_id': self.line_id,
            'extension_id': self.extension_id,
            'main_user': self.main_user,
            'main_line': self.main_line
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'],
                   msg['user_id'],
                   msg['line_id'],
                   msg['extension_id'],
                   msg['main_user'],
                   msg['main_line'])


class CreateUserLineExtensionEvent(UserLineExtensionConfigEvent):
    name = 'user_line_extension_created'


class EditUserLineExtensionEvent(UserLineExtensionConfigEvent):
    name = 'user_line_extension_edited'


class DeleteUserLineExtensionEvent(UserLineExtensionConfigEvent):
    name = 'user_line_extension_deleted'
