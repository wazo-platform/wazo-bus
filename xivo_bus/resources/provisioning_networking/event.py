# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ArbitraryEvent


class EditProvisioningNetworkingEvent(ArbitraryEvent):

    def __init__(self):
        super(EditProvisioningNetworkingEvent, self).__init__(
            name='provisioning_networking_edited',
            body={},
            required_acl='events.config.provisioning.networking.edited',
        )
        self.routing_key = 'config.provisioning.networking.edited'
