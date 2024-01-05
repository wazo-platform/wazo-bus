# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class ApplicationDict(TypedDict, total=False):
    uuid: str
    tenant_uuid: str
    name: str
    destination: str | None
    destination_options: dict[str, str]
