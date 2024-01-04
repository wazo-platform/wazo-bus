# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class GroupDict(TypedDict, total=False):
    id: int
    uuid: UUIDStr
