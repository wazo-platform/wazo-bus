# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import UserEvent
from ..common.types import UUIDStr


class FavoriteAddedEvent(UserEvent):
    service = 'dird'
    name = 'favorite_added'
    routing_key_fmt = 'directory.{user_uuid}.favorite.created'

    def __init__(
        self,
        source_name: str,
        entry_id: str,
        wazo_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'xivo_uuid': str(wazo_uuid),
            'user_uuid': str(user_uuid),
            'source': source_name,
            'source_entry_id': entry_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class FavoriteDeletedEvent(UserEvent):
    service = 'dird'
    name = 'favorite_deleted'
    routing_key_fmt = 'directory.{user_uuid}.favorite.deleted'

    def __init__(
        self,
        source_name: str,
        entry_id: str,
        wazo_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = {
            'xivo_uuid': str(wazo_uuid),
            'user_uuid': str(user_uuid),
            'source': source_name,
            'source_entry_id': entry_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
