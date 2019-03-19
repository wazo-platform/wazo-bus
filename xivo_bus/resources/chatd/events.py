# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import BaseEvent


class PresenceUpdatedEvent(BaseEvent):

    name = 'chatd_presence_updated'
    routing_key_fmt = 'chatd.users.{uuid}.presences.updated'

    def __init__(self, user):
        self._body = user
        super(PresenceUpdatedEvent, self).__init__()


class UserRoomCreatedEvent(BaseEvent):

    name = 'chatd_user_room_created'
    routing_key_fmt = 'chatd.users.{user_uuid}.rooms.created'

    def __init__(self, user_uuid, room):
        self._body = room
        self.routing_key = self.routing_key_fmt.format(user_uuid=user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)
