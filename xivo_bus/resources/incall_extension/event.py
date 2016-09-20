# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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


class IncallExtensionConfigEvent(ResourceConfigEvent):

    def __init__(self, incall_id, extension_id):
        self.incall_id = incall_id
        self.extension_id = extension_id

    def marshal(self):
        return {
            'incall_id': self.incall_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['incall_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.incall_id == other.incall_id and
                self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not (self == other)


class IncallExtensionAssociatedEvent(IncallExtensionConfigEvent):
    name = 'incall_extension_associated'
    routing_key = 'config.incalls.extensions.updated'


class IncallExtensionDissociatedEvent(IncallExtensionConfigEvent):
    name = 'incall_extension_dissociated'
    routing_key = 'config.incalls.extensions.deleted'
