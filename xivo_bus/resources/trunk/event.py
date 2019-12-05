# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent, ResourceConfigEvent


class TrunkStatusUpdatedEvent(BaseEvent):

    name = 'trunk_status_updated'
    routing_key_fmt = 'trunks.{id}.status.updated'

    def __init__(self, status):
        self._body = status
        super(TrunkStatusUpdatedEvent, self).__init__()


class EditTrunkEvent(ResourceConfigEvent):
    name = 'trunk_edited'
    routing_key = 'config.trunk.edited'


class CreateTrunkEvent(ResourceConfigEvent):
    name = 'trunk_created'
    routing_key = 'config.trunk.created'


class DeleteTrunkEvent(ResourceConfigEvent):
    name = 'trunk_deleted'
    routing_key = 'config.trunk.deleted'
