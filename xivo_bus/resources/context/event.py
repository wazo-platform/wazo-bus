# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique Inc.
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditContextEvent(ResourceConfigEvent):
    name = 'context_edited'
    routing_key = 'config.contexts.edited'


class CreateContextEvent(ResourceConfigEvent):
    name = 'context_created'
    routing_key = 'config.contexts.created'


class DeleteContextEvent(ResourceConfigEvent):
    name = 'context_deleted'
    routing_key = 'config.contexts.deleted'
