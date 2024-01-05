# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class LinePresenceDict(TypedDict, total=False):
    id: int
    state: str


class MessageDict(TypedDict, total=False):
    uuid: str
    content: str
    alias: str
    user_uuid: str
    tenant_uuid: str
    wazo_uuid: str
    created_at: str
    room: RoomDict


class RoomDict(TypedDict, total=False):
    uuid: str
    tenant_uuid: str
    name: str
    users: list[RoomUserDict]


class RoomUserDict(TypedDict, total=False):
    uuid: str
    tenant_uuid: str
    wazo_uuid: str


class UserPresenceDict(TypedDict, total=False):
    uuid: str
    tenant_uuid: str
    state: str
    status: str
    last_activity: str
    line_state: str
    mobile: bool
    do_not_disturb: bool
    connected: bool
    lines: list[LinePresenceDict]
