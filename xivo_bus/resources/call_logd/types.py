# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict


class CallLogExportDataDict(TypedDict, total=False):
    uuid: Annotated[str, {'format': 'uuid'}]
    tenant_uuid: Annotated[str, {'format': 'uuid'}]
    user_uuid: Annotated[str, {'format': 'uuid'}]
    requested_at: Annotated[str, {'format': 'date-time'}]
    filename: str
    status: str
