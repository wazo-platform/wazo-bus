# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_bus.resources.common.event import UserEvent


class CallPushNotificationEvent(UserEvent):
    service = 'calld'
    name = 'call_push_notification'
    routing_key_fmt = 'calls.call.push_notification'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, push_schema, tenant_uuid, user_uuid):
        super().__init__(push_schema, tenant_uuid, user_uuid)


class CallCancelPushNotificationEvent(UserEvent):
    service = 'calld'
    name = 'call_cancel_push_notification'
    routing_key_fmt = 'calls.call.cancel_push_notification'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, push_schema, tenant_uuid, user_uuid):
        super().__init__(push_schema, tenant_uuid, user_uuid)
