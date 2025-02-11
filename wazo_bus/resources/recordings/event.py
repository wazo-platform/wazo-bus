# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import RecordingsAnnouncementsDict


class RecordingsAnnouncementsEditedEvent(TenantEvent):
    service = 'confd'
    name = 'recordings_announcements_edited'
    routing_key_fmt = 'config.recordings.announcements.edited'

    def __init__(
        self,
        recordings_announcements: RecordingsAnnouncementsDict,
        tenant_uuid: UUIDStr,
    ) -> None:
        super().__init__(recordings_announcements, tenant_uuid)
