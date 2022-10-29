# -*- coding: utf-8 -*-
# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent, UserEvent


class PresenceUpdatedEvent(TenantEvent):
    service = 'chatd'
    name = 'chatd_presence_updated'
    routing_key_fmt = 'chatd.users.{uuid}.presences.updated'

    def __init__(self, user_presence_data, tenant_uuid):
        super(PresenceUpdatedEvent, self).__init__(user_presence_data, tenant_uuid)


class UserRoomCreatedEvent(UserEvent):
    service = 'chatd'
    name = 'chatd_user_room_created'
    routing_key_fmt = 'chatd.users.{user_uuid}.rooms.created'

    def __init__(self, room_data, tenant_uuid, user_uuid):
        super(UserRoomCreatedEvent, self).__init__(room_data, tenant_uuid, user_uuid)


class UserRoomMessageCreatedEvent(UserEvent):
    service = 'chatd'
    name = 'chatd_user_room_message_created'
    routing_key_fmt = 'chatd.users.{user_uuid}.rooms.{room_uuid}.messages.created'

    def __init__(self, message_data, room_uuid, tenant_uuid, user_uuid):
        super(UserRoomMessageCreatedEvent, self).__init__(
            message_data, tenant_uuid, user_uuid
        )
        if room_uuid is None:
            raise ValueError('room_uuid must have a value')
        self.room_uuid = str(room_uuid)


class UserRoomActivityEvent(UserEvent):
    service = 'chatd'
    name = 'chatd_user_room_activity_created'
    routing_key_fmt = 'chatd.users.{user_uuid}.rooms.{room_uuid}.activities.created'

    def __init__(self, activity, room_uuid, tenant_uuid, user_uuid):
        super(UserRoomActivityEvent, self).__init__(
            activity, tenant_uuid, user_uuid
        )
        if room_uuid is None:
            raise ValueError('room_uuid must have a value')
        self.room_uuid = str(room_uuid)
