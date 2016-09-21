# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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


class LineExtensionConfigEvent(ResourceConfigEvent):
    routing_key = 'config.line_extension_association.{}'

    def __init__(self,
                 line_id,
                 extension_id):
        self.line_id = int(line_id)
        self.extension_id = int(extension_id)

    def marshal(self):
        return {
            'line_id': self.line_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['line_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.line_id == other.line_id and
                self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not (self == other)


class LineExtensionAssociatedEvent(LineExtensionConfigEvent):
    name = 'line_extension_associated'
    routing_key = LineExtensionConfigEvent.routing_key.format('created')


class LineExtensionDissociatedEvent(LineExtensionConfigEvent):
    name = 'line_extension_dissociated'
    routing_key = LineExtensionConfigEvent.routing_key.format('deleted')
