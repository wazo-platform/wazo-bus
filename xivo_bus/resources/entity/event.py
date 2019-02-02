# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class CreateEntityEvent(ResourceConfigEvent):
    name = 'entity_created'
    routing_key = 'config.entity.created'


class EditEntityEvent(ResourceConfigEvent):
    name = 'entity_edited'
    routing_key = 'config.entity.edited'


class DeleteEntityEvent(ResourceConfigEvent):
    name = 'entity_deleted'
    routing_key = 'config.entity.deleted'
