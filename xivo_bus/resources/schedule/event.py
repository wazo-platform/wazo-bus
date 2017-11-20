# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditScheduleEvent(ResourceConfigEvent):
    name = 'schedule_edited'
    routing_key = 'config.schedules.edited'


class CreateScheduleEvent(ResourceConfigEvent):
    name = 'schedule_created'
    routing_key = 'config.schedules.created'


class DeleteScheduleEvent(ResourceConfigEvent):
    name = 'schedule_deleted'
    routing_key = 'config.schedules.deleted'
