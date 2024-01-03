# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict

from ..common.types import Format


class GroupDict(TypedDict, total=False):
    id: int
    uuid: Annotated[str, Format('uuid')]
