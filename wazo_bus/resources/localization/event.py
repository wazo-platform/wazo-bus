# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import LocalizationDict


class LocalizationEditedEvent(TenantEvent):
    service = 'confd'
    name = 'localization_edited'
    routing_key_fmt = 'config.localization.edited'

    def __init__(self, localization: LocalizationDict, tenant_uuid: UUIDStr) -> None:
        super().__init__(localization, tenant_uuid)
