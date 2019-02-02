# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class DeviceConfigEvent(ResourceConfigEvent):
    routing_key = 'config.device.{}'

    def __init__(self, device_id):
        self.id = device_id


class EditDeviceEvent(DeviceConfigEvent):
    name = 'device_edited'
    routing_key = DeviceConfigEvent.routing_key.format('edited')


class CreateDeviceEvent(DeviceConfigEvent):
    name = 'device_created'
    routing_key = DeviceConfigEvent.routing_key.format('created')


class DeleteDeviceEvent(DeviceConfigEvent):
    name = 'device_deleted'
    routing_key = DeviceConfigEvent.routing_key.format('deleted')
