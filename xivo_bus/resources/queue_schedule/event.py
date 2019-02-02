# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class QueueScheduleConfigEvent(object):

    def __init__(self, queue_id, schedule_id):
        self.queue_id = queue_id
        self.schedule_id = schedule_id

    def marshal(self):
        return {
            'queue_id': self.queue_id,
            'schedule_id': self.schedule_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['queue_id'],
            msg['schedule_id'])

    def __eq__(self, other):
        return (self.queue_id == other.queue_id
                and self.schedule_id == other.schedule_id)

    def __ne__(self, other):
        return not self == other


class QueueScheduleAssociatedEvent(QueueScheduleConfigEvent):
    name = 'queue_schedule_associated'
    routing_key = 'config.queues.schedules.updated'


class QueueScheduleDissociatedEvent(QueueScheduleConfigEvent):
    name = 'queue_schedule_dissociated'
    routing_key = 'config.queues.schedules.deleted'
