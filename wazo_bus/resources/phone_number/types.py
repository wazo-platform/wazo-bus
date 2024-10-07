# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class PhoneNumberDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    number: str
    caller_id_name: str | None
    main: bool
    shareable: bool
