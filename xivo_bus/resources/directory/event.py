# -*- coding: utf-8 -*-

# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>


class _BaseFavoriteEvent(object):

    def __init__(self, xivo_uuid, user_uuid, source, source_entry_id):
        self.routing_key = self._routing_key_fmt.format(user_uuid)
        self.required_acl = self._required_acl_fmt.format(user_uuid)
        self._xivo_uuid = xivo_uuid
        self._user_uuid = user_uuid
        self._source = source
        self._source_entry_id = source_entry_id

    def marshal(self):
        return {
            'xivo_uuid': self._xivo_uuid,
            'user_uuid': self._user_uuid,
            'source': self._source,
            'source_entry_id': self._source_entry_id,
        }


class FavoriteAddedEvent(_BaseFavoriteEvent):

    name = 'favorite_added'
    _routing_key_fmt = 'directory.{}.favorite.created'
    _required_acl_fmt = 'event.directory.{}.favorite.created'


class FavoriteDeletedEvent(_BaseFavoriteEvent):

    name = 'favorite_deleted'
    _routing_key_fmt = 'directory.{}.favorite.deleted'
    _required_acl_fmt = 'event.directory.{}.favorite.deleted'
