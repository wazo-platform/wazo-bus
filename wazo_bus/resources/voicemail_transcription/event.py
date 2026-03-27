# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import TranscriptionCompletedPayload


class VoicemailTranscriptionCompletedEvent(TenantEvent):
    service = 'webhookd'
    name = 'voicemail_transcription_completed'
    routing_key_fmt = 'voicemails.transcriptions.completed'

    def __init__(
        self,
        transcription: TranscriptionCompletedPayload,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(transcription, tenant_uuid)
