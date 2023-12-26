# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    username: str


class EndpointSIPLineDict(TypedDict, total=False):
    id: int


class EndpointSIPTrunkDict(TypedDict, total=False):
    id: int


class EndpointSIPRegistrationSectionOptionsDict(TypedDict, total=False):
    client_uri: str


class EndpointSIPDict(TypedDict, total=False):
    uuid: str
    tenant_uuid: str
    name: str
    label: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict
    regsitration_section_options: EndpointSIPRegistrationSectionOptionsDict
    trunk: EndpointSIPTrunkDict
    line: EndpointSIPLineDict
