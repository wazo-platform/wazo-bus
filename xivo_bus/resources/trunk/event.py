# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditTrunkEvent(ResourceConfigEvent):
    name = 'trunk_edited'
    routing_key = 'config.trunk.edited'


class CreateTrunkEvent(ResourceConfigEvent):
    name = 'trunk_created'
    routing_key = 'config.trunk.created'


class DeleteTrunkEvent(ResourceConfigEvent):
    name = 'trunk_deleted'
    routing_key = 'config.trunk.deleted'
