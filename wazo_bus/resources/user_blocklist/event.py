# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from wazo_bus.resources.common.event import UserEvent
from wazo_bus.resources.common.types import UUIDStr


class BlocklistNumberInfo(TypedDict):
    uuid: str
    user_uuid: str
    number: str
    label: str | None
    blocklist_uuid: str


class UserBlocklistNumberCreatedEvent(UserEvent):
    routing_key_fmt = 'confd.users.{user_uuid}.blocklist.created'
    name = 'user_blocklist_number_created'

    def __init__(
        self,
        blocklist_number: BlocklistNumberInfo,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        super().__init__(blocklist_number, tenant_uuid, user_uuid)


class UserBlocklistNumberEditedEvent(UserEvent):
    routing_key_fmt = 'confd.users.{user_uuid}.blocklist.edited'
    name = 'user_blocklist_number_edited'

    def __init__(
        self,
        blocklist_number: BlocklistNumberInfo,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        super().__init__(blocklist_number, tenant_uuid, user_uuid)


class UserBlocklistNumberDeletedEvent(UserEvent):
    routing_key_fmt = 'confd.users.{user_uuid}.blocklist.deleted'
    name = 'user_blocklist_number_deleted'

    def __init__(
        self,
        blocklist_number: BlocklistNumberInfo,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ) -> None:
        super().__init__(blocklist_number, tenant_uuid, user_uuid)
