# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class LinePresenceDict(TypedDict, total=False):
    id: int
    state: str


class MessageDict(TypedDict, total=False):
    uuid: UUIDStr
    content: str
    alias: str
    user_uuid: UUIDStr
    tenant_uuid: UUIDStr
    wazo_uuid: UUIDStr
    created_at: str
    room: RoomDict


class RoomDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    name: str
    users: list[RoomUserDict]


class RoomUserDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    wazo_uuid: UUIDStr


class UserPresenceDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    state: str
    status: str
    last_activity: str
    line_state: str
    mobile: bool
    do_not_disturb: bool
    connected: bool
    lines: list[LinePresenceDict]
