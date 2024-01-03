# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict


class ApplicationDict(TypedDict, total=False):
    uuid: Annotated[str, {'format': 'uuid'}]


class LineEndpointSIPDict(TypedDict, total=False):
    uuid: Annotated[str, {'format': 'uuid'}]


class LineEndpointSCCPDict(TypedDict, total=False):
    id: int


class LineEndpointCustomDict(TypedDict, total=False):
    id: int


class LineDict(TypedDict, total=False):
    id: int
    name: str
    endpoint_sip: LineEndpointSIPDict
    endpoint_sccp: LineEndpointSCCPDict
    endpoint_custom: LineEndpointCustomDict
