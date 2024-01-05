# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    username: str


class LineEndpointSIPDict(TypedDict, total=False):
    uuid: str
    tenant_uuid: str
    label: str
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict


class LineEndpointSCCPDict(TypedDict, total=False):
    id: int
    tenant_uuid: str


class LineEndpointCustomDict(TypedDict, total=False):
    id: int
    tenant_uuid: str
    interface: str


class LineDict(TypedDict, total=False):
    id: int
    tenant_uuid: str
    name: str
