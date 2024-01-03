# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict


class PJSIPTransportDict(TypedDict, total=False):
    uuid: Annotated[str, {'format': 'uuid'}]
    name: str
    options: list[str]
