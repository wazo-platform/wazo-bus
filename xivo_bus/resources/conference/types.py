# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class ParticipantDict(TypedDict):
    id: str
    caller_id_name: str
    caller_id_number: str
    muted: bool
    join_time: int
    admin: bool
    language: str
    call_id: str
    user_uuid: str
