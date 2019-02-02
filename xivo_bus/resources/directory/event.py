# -*- coding: utf-8 -*-
# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


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
    _required_acl_fmt = 'events.directory.{}.favorite.created'


class FavoriteDeletedEvent(_BaseFavoriteEvent):

    name = 'favorite_deleted'
    _routing_key_fmt = 'directory.{}.favorite.deleted'
    _required_acl_fmt = 'events.directory.{}.favorite.deleted'
