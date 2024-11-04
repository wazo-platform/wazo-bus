# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import PhoneNumberDict


class PhoneNumberCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'phone_number_created'
    routing_key_fmt = 'config.phone_number.created'

    def __init__(self, phone_number: PhoneNumberDict, tenant_uuid: UUIDStr):
        super().__init__(phone_number, tenant_uuid)


class PhoneNumberDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'phone_number_deleted'
    routing_key_fmt = 'config.phone_number.deleted'

    def __init__(self, phone_number: PhoneNumberDict, tenant_uuid: UUIDStr):
        super().__init__(phone_number, tenant_uuid)


class PhoneNumberEditedEvent(TenantEvent):
    service = 'confd'
    name = 'phone_number_edited'
    routing_key_fmt = 'config.phone_number.edited'

    def __init__(self, phone_number: PhoneNumberDict, tenant_uuid: UUIDStr):
        super().__init__(phone_number, tenant_uuid)


class PhoneNumberMainUpdatedEvent(TenantEvent):
    service = 'confd'
    name = 'phone_number_main_updated'
    routing_key_fmt = 'config.phone_number.main.updated'

    def __init__(
        self,
        current_main_uuid: str | None,
        new_main_uuid: str | None,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(
            {'current_main_uuid': current_main_uuid, 'new_main_uuid': new_main_uuid},
            tenant_uuid,
        )
