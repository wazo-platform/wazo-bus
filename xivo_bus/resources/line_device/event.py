# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseLineDeviceEvent(BaseEvent):

    def __init__(self, line, device):
        self._body = {
            'line': line,
            'device': device,
        }
        super(_BaseLineDeviceEvent, self).__init__()


class LineDeviceAssociatedEvent(_BaseLineDeviceEvent):

    name = 'line_device_associated'
    routing_key_fmt = 'config.lines.{line[id]}.devices.{device[id]}.updated'


class LineDeviceDissociatedEvent(_BaseLineDeviceEvent):

    name = 'line_device_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.devices.{device[id]}.deleted'
