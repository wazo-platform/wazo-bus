# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserFuncKeyEvent(ResourceConfigEvent):

    def __init__(self, func_key_id, user_id):
        self.func_key_id = func_key_id
        self.user_id = user_id

    def marshal(self):
        return {'id': self.func_key_id,
                'destination': 'user',
                'user_id': self.user_id}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['user_id'])


class BSFilterFuncKeyEvent(ResourceConfigEvent):

    def __init__(self, func_key_id, filter_id, secretary_id):
        self.func_key_id = func_key_id
        self.filter_id = filter_id
        self.secretary_id = secretary_id

    def marshal(self):
        return {'id': self.func_key_id,
                'destination': 'bsfilter',
                'filter_id': self.filter_id,
                'secretary_id': self.secretary_id}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['filter_id'], msg['secretary_id'])


class UserCreateFuncKeyEvent(UserFuncKeyEvent):
    name = 'func_key_created'


class UserDeleteFuncKeyEvent(UserFuncKeyEvent):
    name = 'func_key_deleted'


class BSFilterCreateFuncKeyEvent(BSFilterFuncKeyEvent):
    name = 'func_key_created'


class BSFilterDeleteFuncKeyEvent(BSFilterFuncKeyEvent):
    name = 'func_key_deleted'
