# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_bus.resources.common.event import BaseEvent


class PushNotificationEvent(BaseEvent):
    name = 'call_push_notification'
    routing_key_fmt = 'calls.call.push_notification'

    def __init__(self, push_notification, user_uuid):
        self._body = push_notification
        super(PushNotificationEvent, self).__init__()
        self.required_acl = 'events.calls.{uuid}'.format(uuid=user_uuid)
