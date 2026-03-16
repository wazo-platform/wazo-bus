# Copyright 2023-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Literal, TypedDict

from ..common.types import DateTimeStr, UUIDStr


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
    voicemail: VoicemailDict


class VoicemailTranscriptionDict(TypedDict, total=False):
    voicemail_id: int
    message_id: str
    tenant_uuid: UUIDStr
    transcription_text: str
    provider_id: str
    language: str
    duration: float
    created_at: DateTimeStr
