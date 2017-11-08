# -*- coding: utf-8 -*-

# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class IncallScheduleConfigEvent(object):

    def __init__(self, incall_id, schedule_id):
        self.incall_id = incall_id
        self.schedule_id = schedule_id

    def marshal(self):
        return {
            'incall_id': self.incall_id,
            'schedule_id': self.schedule_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['incall_id'],
            msg['schedule_id'])

    def __eq__(self, other):
        return (self.incall_id == other.incall_id and
                self.schedule_id == other.schedule_id)

    def __ne__(self, other):
        return not self == other


class IncallScheduleAssociatedEvent(IncallScheduleConfigEvent):
    name = 'incall_schedule_associated'
    routing_key = 'config.incalls.schedules.updated'


class IncallScheduleDissociatedEvent(IncallScheduleConfigEvent):
    name = 'incall_schedule_dissociated'
    routing_key = 'config.incalls.schedules.deleted'
