# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditIncallEvent(ResourceConfigEvent):
    name = 'incall_edited'
    routing_key = 'config.incalls.edited'


class CreateIncallEvent(ResourceConfigEvent):
    name = 'incall_created'
    routing_key = 'config.incalls.created'


class DeleteIncallEvent(ResourceConfigEvent):
    name = 'incall_deleted'
    routing_key = 'config.incalls.deleted'
