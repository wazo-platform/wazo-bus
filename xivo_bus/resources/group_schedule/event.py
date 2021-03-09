# -*- coding: utf-8 -*-
# Copyright 2017-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class GroupScheduleConfigEvent(BaseEvent):

    def __init__(self, **body):
        self._body = body
        super(GroupScheduleConfigEvent, self).__init__()


class GroupScheduleAssociatedEvent(GroupScheduleConfigEvent):
    name = 'group_schedule_associated'
    routing_key_fmt = 'config.groups.schedules.updated'


class GroupScheduleDissociatedEvent(GroupScheduleConfigEvent):
    name = 'group_schedule_dissociated'
    routing_key_fmt = 'config.groups.schedules.deleted'
