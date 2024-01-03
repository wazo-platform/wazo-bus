# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class CallLogExportDataDict(TypedDict):
    uuid: str
    tenant_uuid: str
    user_uuid: str
    requested_at: str
    filename: str
    status: str