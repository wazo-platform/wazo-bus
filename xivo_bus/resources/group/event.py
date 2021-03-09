# -*- coding: utf-8 -*-
# Copyright 2016-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class _BaseGroupEvent(BaseEvent):

    def __init__(self, **group):
        self._body = group
        super(_BaseGroupEvent, self).__init__()


class EditGroupEvent(_BaseGroupEvent):
    name = 'group_edited'
    routing_key_fmt = 'config.groups.edited'


class CreateGroupEvent(_BaseGroupEvent):
    name = 'group_created'
    routing_key_fmt = 'config.groups.created'


class DeleteGroupEvent(_BaseGroupEvent):
    name = 'group_deleted'
    routing_key_fmt = 'config.groups.deleted'


class EditGroupFallbackEvent(_BaseGroupEvent):
    name = 'group_fallback_edited'
    routing_key_fmt = 'config.groups.fallbacks.edited'
