# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class CallFilterRecipientUsersAssociatedEvent(TenantEvent):
    name = 'call_filter_recipient_users_associated'
    routing_key_fmt = 'config.callfilters.recipients.users.updated'

    def __init__(self, call_filter_id, users, tenant_uuid):
        content = {
            'call_filter_id': call_filter_id,
            'user_uuids': users,
        }
        super(CallFilterRecipientUsersAssociatedEvent, self).__init__(content, tenant_uuid)


class CallFilterSurrogateUsersAssociatedEvent(TenantEvent):
    name = 'call_filter_surrogate_users_associated'
    routing_key_fmt = 'config.callfilters.surrogates.users.updated'

    def __init__(self, call_filter_id, users, tenant_uuid):
        content = {
            'call_filter_id': call_filter_id,
            'user_uuids': users,
        }
        super(CallFilterSurrogateUsersAssociatedEvent, self).__init__(content, tenant_uuid)
