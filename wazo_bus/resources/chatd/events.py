# Copyright 2019-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ..common.event import MultiUserEvent, TenantEvent, UserEvent
from ..common.types import UUIDStr
from .types import (
    DeliveryStatusDict,
    MessageDict,
    RoomDict,
    UserIdentityDict,
    UserPresenceDict,
)


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


class UserIdentityCreatedEvent(UserEvent):
    service = 'chatd'
    name = 'chatd_user_identity_created'
    routing_key_fmt = 'chatd.users.{user_uuid}.identities.created'

    def __init__(
        self,
        identity_data: UserIdentityDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        super().__init__(identity_data, tenant_uuid, user_uuid)


class UserIdentityUpdatedEvent(UserEvent):
    service = 'chatd'
    name = 'chatd_user_identity_updated'
    routing_key_fmt = 'chatd.users.{user_uuid}.identities.updated'

    def __init__(
        self,
        identity_data: UserIdentityDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        super().__init__(identity_data, tenant_uuid, user_uuid)


class UserIdentityDeletedEvent(UserEvent):
    service = 'chatd'
    name = 'chatd_user_identity_deleted'
    routing_key_fmt = 'chatd.users.{user_uuid}.identities.deleted'

    def __init__(
        self,
        identity_data: UserIdentityDict,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        super().__init__(identity_data, tenant_uuid, user_uuid)


class MessageDeliveryStatusEvent(MultiUserEvent):
    service = 'chatd'
    name = 'chatd_message_delivery_status'
    routing_key_fmt = 'chatd.rooms.{room_uuid}.messages.{message_uuid}.delivery'

    def __init__(
        self,
        delivery_data: DeliveryStatusDict,
        room_uuid: UUIDStr,
        message_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ) -> None:
        super().__init__(delivery_data, tenant_uuid, user_uuids)
        self.room_uuid = str(room_uuid)
        self.message_uuid = str(message_uuid)
