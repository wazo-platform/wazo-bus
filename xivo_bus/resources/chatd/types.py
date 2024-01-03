# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict


class LinePresenceDict(TypedDict, total=False):
    id: int
    state: str


class MessageDict(TypedDict, total=False):
    uuid: Annotated[str, {'format': 'uuid'}]
    content: str
    alias: str
    user_uuid: Annotated[str, {'format': 'uuid'}]
    tenant_uuid: Annotated[str, {'format': 'uuid'}]
    wazo_uuid: Annotated[str, {'format': 'uuid'}]
    created_at: str
    room: RoomDict


class RoomDict(TypedDict, total=False):
    uuid: Annotated[str, {'format': 'uuid'}]
    tenant_uuid: Annotated[str, {'format': 'uuid'}]
    name: str
    users: list[RoomUserDict]


class RoomUserDict(TypedDict, total=False):
    uuid: Annotated[str, {'format': 'uuid'}]
    tenant_uuid: Annotated[str, {'format': 'uuid'}]
    wazo_uuid: Annotated[str, {'format': 'uuid'}]


class UserPresenceDict(TypedDict, total=False):
    uuid: Annotated[str, {'format': 'uuid'}]
    tenant_uuid: Annotated[str, {'format': 'uuid'}]
    state: str
    status: str
    last_activity: str
    line_state: str
    mobile: bool
    do_not_disturb: bool
    connected: bool
    lines: list[LinePresenceDict]
