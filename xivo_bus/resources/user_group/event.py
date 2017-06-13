# -*- coding: utf-8 -*-

# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
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


class UserGroupConfigEvent(object):

    def __init__(self, user_uuid, group_ids):
        self.user_uuid = user_uuid
        self.group_ids = group_ids

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'group_ids': self.group_ids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_uuid'],
            msg['group_ids'])

    def __eq__(self, other):
        return (self.user_uuid == other.user_uuid and
                self.group_ids == other.group_ids)

    def __ne__(self, other):
        return not self == other


class UserGroupsAssociatedEvent(UserGroupConfigEvent):
    name = 'groups_associated'
    routing_key = 'config.users.groups.updated'
