# -*- coding: utf-8 -*-
# Copyright 2017-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class GroupCallPermissionConfigEvent(BaseEvent):

    def __init__(self, **body):
        self._body = body
        super(GroupCallPermissionConfigEvent, self).__init__()


class GroupCallPermissionAssociatedEvent(GroupCallPermissionConfigEvent):
    name = 'call_permission_associated'
    routing_key_fmt = 'config.groups.{group_uuid}.callpermissions.updated'


class GroupCallPermissionDissociatedEvent(GroupCallPermissionConfigEvent):
    name = 'call_permission_dissociated'
    routing_key_fmt = 'config.groups.{group_uuid}.callpermissions.deleted'
