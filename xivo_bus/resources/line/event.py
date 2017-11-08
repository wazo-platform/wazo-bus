# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditLineEvent(ResourceConfigEvent):
    name = 'line_edited'
    routing_key = 'config.line.edited'


class CreateLineEvent(ResourceConfigEvent):
    name = 'line_created'
    routing_key = 'config.line.created'


class DeleteLineEvent(ResourceConfigEvent):
    name = 'line_deleted'
    routing_key = 'config.line.deleted'
