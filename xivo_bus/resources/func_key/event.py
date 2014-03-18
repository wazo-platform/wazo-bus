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


class FuncKeyConfigEvent(ResourceConfigEvent):

    def __init__(self, func_key_id, func_key_type, destination, destination_id):
        self.id = int(func_key_id)
        self.type = func_key_type
        self.destination = destination
        self.destination_id = destination_id

    def marshal(self):
        return {
            'id': self.id,
            'type': self.type,
            'destination': self.destination,
            'destination_id': self.destination_id
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['type'], msg['destination'], msg['destination_id'])


class CreateFuncKeyEvent(FuncKeyConfigEvent):
    name = 'func_key_created'
