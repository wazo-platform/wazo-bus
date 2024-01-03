# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict


class EndpointSIPDict(TypedDict, total=False):
    uuid: Annotated[str, {'format': 'uuid'}]
    tenant_uuid: Annotated[str, {'format': 'uuid'}]
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict
    registration_section_options: EndpointSIPRegistrationSectionOptionsDict


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    username: str


class EndpointSIPRegistrationSectionOptionsDict(TypedDict, total=False):
    client_uri: str


class EndpointIAXDict(TypedDict, total=False):
    id: int
    tenant_uuid: Annotated[str, {'format': 'uuid'}]
    name: str


class EndpointCustomDict(TypedDict, total=False):
    id: int
    tenant_uuid: Annotated[str, {'format': 'uuid'}]
    interface: str


class TrunkDict(TypedDict, total=False):
    id: int
    tenant_uuid: Annotated[str, {'format': 'uuid'}]
