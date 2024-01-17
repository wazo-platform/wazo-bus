# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Literal, TypedDict


class PluginErrorDict(TypedDict, total=False):
    error_id: str
    message: str
    resource: Literal['plugins']
    details: dict
