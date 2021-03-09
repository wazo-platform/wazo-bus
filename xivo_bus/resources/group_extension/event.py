# -*- coding: utf-8 -*-
# Copyright 2016-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class GroupExtensionConfigEvent(BaseEvent):

    def __init__(self, **body):
        self._body = body
        super(GroupExtensionConfigEvent, self).__init__()


class GroupExtensionAssociatedEvent(GroupExtensionConfigEvent):
    name = 'group_extension_associated'
    routing_key_fmt = 'config.groups.extensions.updated'


class GroupExtensionDissociatedEvent(GroupExtensionConfigEvent):
    name = 'group_extension_dissociated'
    routing_key_fmt = 'config.groups.extensions.deleted'
