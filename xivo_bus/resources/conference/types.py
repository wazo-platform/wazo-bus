# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict

from ..common.types import Format


class ParticipantDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_number: str
    muted: bool
    join_time: int
    admin: bool
    language: str
    call_id: str
    user_uuid: Annotated[str, Format('uuid')]
