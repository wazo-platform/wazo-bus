# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class OutcallScheduleConfigEvent(object):

    def __init__(self, outcall_id, schedule_id):
        self.outcall_id = outcall_id
        self.schedule_id = schedule_id

    def marshal(self):
        return {
            'outcall_id': self.outcall_id,
            'schedule_id': self.schedule_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['outcall_id'],
            msg['schedule_id'])

    def __eq__(self, other):
        return (self.outcall_id == other.outcall_id
                and self.schedule_id == other.schedule_id)

    def __ne__(self, other):
        return not self == other


class OutcallScheduleAssociatedEvent(OutcallScheduleConfigEvent):
    name = 'outcall_schedule_associated'
    routing_key = 'config.outcalls.schedules.updated'


class OutcallScheduleDissociatedEvent(OutcallScheduleConfigEvent):
    name = 'outcall_schedule_dissociated'
    routing_key = 'config.outcalls.schedules.deleted'
