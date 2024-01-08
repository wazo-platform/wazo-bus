# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class TenantDict(TypedDict, total=False):
    uuid: UUIDStr
    name: str
    slug: str
    domain_names: list[str]
