# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class CallFilterRecipientUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_filter_recipient_users_associated'
    routing_key_fmt = 'config.callfilters.recipients.users.updated'

    def __init__(self, call_filter_id, users, tenant_uuid):
        content = {
            'call_filter_id': call_filter_id,
            'user_uuids': users,
        }
        super(CallFilterRecipientUsersAssociatedEvent, self).__init__(content, tenant_uuid)


class CallFilterSurrogateUsersAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'call_filter_surrogate_users_associated'
    routing_key_fmt = 'config.callfilters.surrogates.users.updated'

    def __init__(self, call_filter_id, users, tenant_uuid):
        content = {
            'call_filter_id': call_filter_id,
            'user_uuids': users,
        }
        super(CallFilterSurrogateUsersAssociatedEvent, self).__init__(content, tenant_uuid)
