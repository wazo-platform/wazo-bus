# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class IngressHTTPDict(TypedDict, total=False):
    uuid: str
    tenant_uuid: str
    uri: str
