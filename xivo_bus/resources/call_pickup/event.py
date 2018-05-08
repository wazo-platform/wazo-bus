# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditCallPickupEvent(ResourceConfigEvent):
    name = 'call_pickup_edited'
    routing_key = 'config.callpickup.edited'


class CreateCallPickupEvent(ResourceConfigEvent):
    name = 'call_pickup_created'
    routing_key = 'config.callpickup.created'


class DeleteCallPickupEvent(ResourceConfigEvent):
    name = 'call_pickup_deleted'
    routing_key = 'config.callpickup.deleted'
