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


class ContextConfigEvent(ResourceConfigEvent):

    def __init__(self, context_id, context_name, display_name, description, context_type):
        self.id = int(context_id)
        self.context_name = context_name
        self.display_name = display_name
        self.description = description
        self.context_type = context_type

    def marshal(self):
        return {
            'id': self.id,
            'name': self.context_name,
            'display_name': self.display_name,
            'description': self.description,
            'type': self.context_type
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['name'], msg['display_name'], msg['description'], msg['type'])


class CreateContextEvent(ContextConfigEvent):
    name = 'context_created'
