# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class EndpointIAXTrunkDict(TypedDict, total=False):
    id: int


class EndpointIAXDict(TypedDict, total=False):
    id: int
    tenant_uuid: UUIDStr
    trunk: EndpointIAXTrunkDict
