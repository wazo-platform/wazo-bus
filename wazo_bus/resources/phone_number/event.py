# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
