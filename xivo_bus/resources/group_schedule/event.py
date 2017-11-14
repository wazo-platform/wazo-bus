# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class GroupScheduleConfigEvent(object):

    def __init__(self, group_id, schedule_id):
        self.group_id = group_id
        self.schedule_id = schedule_id

    def marshal(self):
        return {
            'group_id': self.group_id,
            'schedule_id': self.schedule_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['group_id'],
            msg['schedule_id'])

    def __eq__(self, other):
        return (self.group_id == other.group_id and
                self.schedule_id == other.schedule_id)

    def __ne__(self, other):
        return not self == other


class GroupScheduleAssociatedEvent(GroupScheduleConfigEvent):
    name = 'group_schedule_associated'
    routing_key = 'config.groups.schedules.updated'


class GroupScheduleDissociatedEvent(GroupScheduleConfigEvent):
    name = 'group_schedule_dissociated'
    routing_key = 'config.groups.schedules.deleted'
