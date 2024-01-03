# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict

from ..common.types import Format


class EndpointSIPAuthSectionOptionsDict(TypedDict, total=False):
    username: str


class LineEndpointSIPDict(TypedDict, total=False):
    uuid: Annotated[str, Format('uuid')]
    tenant_uuid: Annotated[str, Format('uuid')]
    label: str
    name: str
    auth_section_options: EndpointSIPAuthSectionOptionsDict


class LineEndpointSCCPDict(TypedDict, total=False):
    id: int
    tenant_uuid: Annotated[str, Format('uuid')]


class LineEndpointCustomDict(TypedDict, total=False):
    id: int
    tenant_uuid: Annotated[str, Format('uuid')]
    interface: str


class LineDict(TypedDict, total=False):
    id: int
    tenant_uuid: Annotated[str, Format('uuid')]
    name: str
