# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict

from ..common.types import Format


class CallLogExportDataDict(TypedDict, total=False):
    uuid: Annotated[str, Format('uuid')]
    tenant_uuid: Annotated[str, Format('uuid')]
    user_uuid: Annotated[str, Format('uuid')]
    requested_at: Annotated[str, Format('date-time')]
    filename: str
    status: str
