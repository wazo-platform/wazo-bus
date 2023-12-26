# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class EndpointIAXTrunkDict(TypedDict):
    id: int


class EndpointIAXDict(TypedDict, total=False):
    id: int
    tenant_uuid: str
    trunk: EndpointIAXTrunkDict
