# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class CallFilterRecipientUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_filter_recipient_users_associated'
    routing_key_fmt = 'config.callfilters.recipients.users.updated'

    def __init__(
        self,
        call_filter_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_filter_id': call_filter_id,
            'user_uuids': users,
        }
        super().__init__(content, tenant_uuid)


class CallFilterSurrogateUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_filter_surrogate_users_associated'
    routing_key_fmt = 'config.callfilters.surrogates.users.updated'

    def __init__(
        self,
        call_filter_id: int,
        users: list[str],
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_filter_id': call_filter_id,
            'user_uuids': users,
        }
        super().__init__(content, tenant_uuid)
