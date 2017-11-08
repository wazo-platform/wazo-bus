# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditOutcallEvent(ResourceConfigEvent):
    name = 'outcall_edited'
    routing_key = 'config.outcalls.edited'


class CreateOutcallEvent(ResourceConfigEvent):
    name = 'outcall_created'
    routing_key = 'config.outcalls.created'


class DeleteOutcallEvent(ResourceConfigEvent):
    name = 'outcall_deleted'
    routing_key = 'config.outcalls.deleted'
