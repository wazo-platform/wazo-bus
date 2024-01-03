# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from xivo_bus.resources.common.event import UserEvent


class FavoriteAddedEvent(UserEvent):
    service = 'dird'
    name = 'favorite_added'
    routing_key_fmt = 'directory.{user_uuid}.favorite.created'

    def __init__(
        self,
        source_name: str,
        entry_id: str,
        wazo_uuid: Annotated[str, {'format': 'uuid'}],
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
        user_uuid: Annotated[str, {'format': 'uuid'}],
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
        wazo_uuid: Annotated[str, {'format': 'uuid'}],
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
        user_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'xivo_uuid': str(wazo_uuid),
            'user_uuid': str(user_uuid),
            'source': source_name,
            'source_entry_id': entry_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
