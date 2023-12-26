# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class VoicemailFolderDict(TypedDict, total=False):
    id: int
    name: str
    type: str


class VoicemailMessageDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_num: str
    duration: int
    tiemstamp: int
    folder: VoicemailFolderDict
