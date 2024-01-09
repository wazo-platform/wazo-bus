# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ..common.event import TenantEvent, UserEvent
from ..common.types import UUIDStr
from .types import MessageDict, RoomDict, UserPresenceDict


class PresenceUpdatedEvent(TenantEvent):
    service = 'chatd'
    name = 'chatd_presence_updated'
    routing_key_fmt = 'chatd.users.{uuid}.presences.updated'

    def __init__(
        self,
        user_presence_data: UserPresenceDict,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(user_presence_data, tenant_uuid)


class UserRoomCreatedEvent(UserEvent):
    service = 'chatd'
    name = 'chatd_user_room_created'
    routing_key_fmt = 'chatd.users.{user_uuid}.rooms.created'

    def __init__(
        self,
        room_data: RoomDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        super().__init__(room_data, tenant_uuid, user_uuid)


class UserRoomMessageCreatedEvent(UserEvent):
    service = 'chatd'
    name = 'chatd_user_room_message_created'
    routing_key_fmt = 'chatd.users.{user_uuid}.rooms.{room_uuid}.messages.created'

    def __init__(
        self,
        message_data: MessageDict,
        room_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        super().__init__(message_data, tenant_uuid, user_uuid)
        if room_uuid is None:
            raise ValueError('room_uuid must have a value')
        self.room_uuid = str(room_uuid)
