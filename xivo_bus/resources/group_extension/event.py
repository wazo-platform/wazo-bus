# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique Inc.
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


class GroupExtensionConfigEvent(object):

    def __init__(self, group_id, extension_id):
        self.group_id = group_id
        self.extension_id = extension_id

    def marshal(self):
        return {
            'group_id': self.group_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['group_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.group_id == other.group_id and
                self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not self == other


class GroupExtensionAssociatedEvent(GroupExtensionConfigEvent):
    name = 'group_extension_associated'
    routing_key = 'config.groups.extensions.updated'


class GroupExtensionDissociatedEvent(GroupExtensionConfigEvent):
    name = 'group_extension_dissociated'
    routing_key = 'config.groups.extensions.deleted'
