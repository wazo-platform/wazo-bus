# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict

from ..common.types import Format


class MOHDict(TypedDict, total=False):
    uuid: Annotated[str, Format('uuid')]
    tenant_uuid: Annotated[str, Format('uuid')]
    name: str
