# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class EndpointSIPDict(TypedDict, total=False):
    uuid: str
    tenant_uuid: str
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict
    registration_section_options: EndpointSIPRegistrationSectionOptionsDict


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    username: str


class EndpointSIPRegistrationSectionOptionsDict(TypedDict, total=False):
    client_uri: str


class EndpointIAXDict(TypedDict, total=False):
    id: int
    tenant_uuid: str
    name: str


class EndpointCustomDict(TypedDict, total=False):
    id: int
    tenant_uuid: str
    interface: str


class TrunkDict(TypedDict, total=False):
    id: int
    tenant_uuid: str
