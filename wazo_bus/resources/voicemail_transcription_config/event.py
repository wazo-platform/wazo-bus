# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class VoicemailTranscriptionConfigBody(TypedDict):
    enabled: bool


class VoicemailTranscriptionConfigEditedEvent(TenantEvent):
    service = 'confd'
    name = 'voicemail_transcription_config_edited'
    routing_key_fmt = 'config.voicemail_transcription.edited'

    def __init__(
        self, content: VoicemailTranscriptionConfigBody, tenant_uuid: UUIDStr
    ) -> None:
        super().__init__(content, tenant_uuid)
