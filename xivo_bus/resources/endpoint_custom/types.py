# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class EndpointCustomLineDict(TypedDict):
    id: int


class EndpointCustomTrunkDict(TypedDict):
    id: int


class EndpointCustomDict(TypedDict, total=False):
    id: int
    tenant_uuid: str
    interface: str
    trunk: EndpointCustomTrunkDict
    line: EndpointCustomLineDict
