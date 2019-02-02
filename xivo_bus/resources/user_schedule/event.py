# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class UserScheduleConfigEvent(object):

    def __init__(self, user_uuid, schedule_id):
        self.user_uuid = user_uuid
        self.schedule_id = schedule_id

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'schedule_id': self.schedule_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_uuid'],
            msg['schedule_id'])

    def __eq__(self, other):
        return (self.user_uuid == other.user_uuid
                and self.schedule_id == other.schedule_id)

    def __ne__(self, other):
        return not self == other


class UserScheduleAssociatedEvent(UserScheduleConfigEvent):
    name = 'user_schedule_associated'
    routing_key = 'config.users.schedules.updated'


class UserScheduleDissociatedEvent(UserScheduleConfigEvent):
    name = 'user_schedule_dissociated'
    routing_key = 'config.users.schedules.deleted'
