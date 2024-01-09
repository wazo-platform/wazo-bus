# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from ..common.types import UUIDStr


class EndpointSIPDict(TypedDict, total=False):
    uuid: UUIDStr
    tenant_uuid: UUIDStr
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict
    registration_section_options: EndpointSIPRegistrationSectionOptionsDict


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    username: str


class EndpointSIPRegistrationSectionOptionsDict(TypedDict, total=False):
    client_uri: str


class EndpointIAXDict(TypedDict, total=False):
    id: int
    tenant_uuid: UUIDStr
    name: str


class EndpointCustomDict(TypedDict, total=False):
    id: int
    tenant_uuid: UUIDStr
    interface: str


class TrunkDict(TypedDict, total=False):
    id: int
    tenant_uuid: UUIDStr
