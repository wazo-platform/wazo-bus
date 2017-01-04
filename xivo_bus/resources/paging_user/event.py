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


class PagingMemberUserConfigEvent(object):

    def __init__(self, paging_id, user_uuids):
        self.paging_id = paging_id
        self.user_uuids = user_uuids

    def marshal(self):
        return {
            'paging_id': self.paging_id,
            'user_uuids': self.user_uuids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['paging_id'],
            msg['user_uuids'])

    def __eq__(self, other):
        return (self.paging_id == other.paging_id and
                self.user_uuids == other.user_uuids)

    def __ne__(self, other):
        return not self == other


class PagingCallerUsersAssociatedEvent(PagingMemberUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.pagings.callers.users.updated'


class PagingMemberUsersAssociatedEvent(PagingMemberUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.pagings.members.users.updated'
