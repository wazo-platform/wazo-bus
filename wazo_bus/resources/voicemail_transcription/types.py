# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from ..common.types import DateTimeStr, UUIDStr


class TranscriptionCompletedPayload(TypedDict, total=False):
    message_id: str
    tenant_uuid: UUIDStr
    voicemail_id: int
    transcription_text: str
    provider_id: str
    language: str
    duration: float
    completed_at: DateTimeStr
