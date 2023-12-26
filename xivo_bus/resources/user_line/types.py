# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class EndpointCustomDict(TypedDict, total=False):
    id: int


class EndpointSCCPDict(TypedDict, total=False):
    id: int


class EndpointSIPDict(TypedDict, total=False):
    uuid: str


class LineDict(TypedDict, total=False):
    id: int
    name: str
    endpoint_sip: EndpointSIPDict
    endpoint_sccp: EndpointSCCPDict
    endpoint_custom: EndpointCustomDict


class UserDict(TypedDict, total=False):
    id: int
    uuid: str
    tenant_uuid: str
