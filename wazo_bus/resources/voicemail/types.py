# Copyright 2023-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Literal, TypedDict


class VoicemailDict(TypedDict, total=False):
    id: int
    name: str
    accesstype: Literal["global", "personal"]


class VoicemailFolderDict(TypedDict, total=False):
    id: int
    name: str
    accesstype: str


class VoicemailMessageDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_num: str
    duration: int
    timestamp: int
    folder: VoicemailFolderDict


class UnifiedVoicemailMessageDict(VoicemailMessageDict, total=False):
    voicemail: VoicemailDict
