# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class EditProvisioningNetworkingEvent(BaseEvent):

    name = 'provisioning_networking_edited'
    routing_key_fmt = 'config.provisioning.networking.edited'

    def __init__(self):
        self._body = {}
        super(EditProvisioningNetworkingEvent, self).__init__()
