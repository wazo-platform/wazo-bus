# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditQueueEvent(ResourceConfigEvent):
    name = 'queue_edited'
    routing_key = 'config.queue.edited'


class CreateQueueEvent(ResourceConfigEvent):
    name = 'queue_created'
    routing_key = 'config.queue.created'


class DeleteQueueEvent(ResourceConfigEvent):
    name = 'queue_deleted'
    routing_key = 'config.queue.deleted'
