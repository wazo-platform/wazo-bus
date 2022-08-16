# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent, UserEvent


class CallLogCreatedEvent(TenantEvent):
    name = 'call_log_created'
    routing_key_fmt = 'call_log.created'

    def __init__(self, cdr_data, tenant_uuid):
        super(CallLogCreatedEvent, self).__init__(cdr_data, tenant_uuid)


class CallLogUserCreatedEvent(UserEvent):
    name = 'call_log_user_created'
    routing_key_fmt = 'call_log.user.{user_uuid}.created'

    def __init__(self, cdr_data, tenant_uuid, user_uuid):
        super(CallLogUserCreatedEvent, self).__init__(
            cdr_data, tenant_uuid, user_uuid
        )
