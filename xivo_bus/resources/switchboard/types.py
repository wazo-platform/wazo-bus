# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Any, TypedDict


class ExtensionDict(TypedDict, total=False):
    id: int
    exten: str
    context: str


class IncallDict(TypedDict, total=False):
    id: int
    extensions: list[ExtensionDict]


class HeldCallDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_number: str


class QueuedCallDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_number: str


class SwitchboardDict(TypedDict, total=False):
    uuid: str
    tenant_uuid: str
    name: str
    timeout: int
    queue_music_on_hold: str
    waiting_room_music_on_hold: str
    extensions: ExtensionDict
    incalls: list[IncallDict]
    user_members: list[UserDict]
    fallbacks: list[SwitchboardFallbackDict]


class SwitchboardFallbackDict(TypedDict, total=False):
    noanswer_destination: Any | None


class UserDict(TypedDict, total=False):
    uuid: str
    firstname: str
    lastname: str
