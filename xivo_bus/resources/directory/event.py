# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import UserEvent


class FavoriteAddedEvent(UserEvent):
    name = 'favorite_added'
    routing_key_fmt = 'directory.{user_uuid}.favorite.created'

    def __init__(self, source_name, entry_id, wazo_uuid, tenant_uuid, user_uuid):
        content = {
            'xivo_uuid': str(wazo_uuid),
            'user_uuid': str(user_uuid),
            'source': source_name,
            'source_entry_id': entry_id,
        }
        super(FavoriteAddedEvent, self).__init__(content, tenant_uuid, user_uuid)


class FavoriteDeletedEvent(UserEvent):
    name = 'favorite_deleted'
    routing_key_fmt = 'directory.{user_uuid}.favorite.deleted'

    def __init__(self, source_name, entry_id, wazo_uuid, tenant_uuid, user_uuid):
        content = {
            'xivo_uuid': str(wazo_uuid),
            'user_uuid': str(user_uuid),
            'source': source_name,
            'source_entry_id': entry_id,
        }
        super(FavoriteDeletedEvent, self).__init__(content, tenant_uuid, user_uuid)
