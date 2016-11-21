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


class GroupMemberUserConfigEvent(object):

    def __init__(self, group_id, user_uuids):
        self.group_id = group_id
        self.user_uuids = user_uuids

    def marshal(self):
        return {
            'group_id': self.group_id,
            'user_uuids': self.user_uuids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['group_id'],
            msg['user_uuids'])

    def __eq__(self, other):
        return (self.group_id == other.group_id and
                self.user_uuids == other.user_uuids)

    def __ne__(self, other):
        return not self == other


class GroupMemberUsersAssociatedEvent(GroupMemberUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.groups.members.users.updated'
