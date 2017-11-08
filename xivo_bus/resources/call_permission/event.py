# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditCallPermissionEvent(ResourceConfigEvent):
    name = 'call_permission_edited'
    routing_key = 'config.callpermission.edited'


class CreateCallPermissionEvent(ResourceConfigEvent):
    name = 'call_permission_created'
    routing_key = 'config.callpermission.created'


class DeleteCallPermissionEvent(ResourceConfigEvent):
    name = 'call_permission_deleted'
    routing_key = 'config.callpermission.deleted'
