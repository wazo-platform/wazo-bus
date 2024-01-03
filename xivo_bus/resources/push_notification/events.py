# Copyright 2022-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from typing import Annotated

from ..common.event import UserEvent
from .types import PushMobileDict


class CallPushNotificationEvent(UserEvent):
    service = 'calld'
    name = 'call_push_notification'
    routing_key_fmt = 'calls.call.push_notification'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(
        self,
        push: PushMobileDict,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
        user_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        super().__init__(push, tenant_uuid, user_uuid)


class CallCancelPushNotificationEvent(UserEvent):
    service = 'calld'
    name = 'call_cancel_push_notification'
    routing_key_fmt = 'calls.call.cancel_push_notification'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(
        self,
        push: PushMobileDict,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
        user_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        super().__init__(push, tenant_uuid, user_uuid)
