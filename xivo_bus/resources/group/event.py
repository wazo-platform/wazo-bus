# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique Inc.
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditGroupEvent(ResourceConfigEvent):
    name = 'group_edited'
    routing_key = 'config.groups.edited'


class CreateGroupEvent(ResourceConfigEvent):
    name = 'group_created'
    routing_key = 'config.groups.created'


class DeleteGroupEvent(ResourceConfigEvent):
    name = 'group_deleted'
    routing_key = 'config.groups.deleted'


class EditGroupFallbackEvent(ResourceConfigEvent):
    name = 'group_fallback_edited'
    routing_key = 'config.groups.fallbacks.edited'
