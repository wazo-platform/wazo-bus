# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ArbitraryEvent


class EditDHCPEvent(ArbitraryEvent):

    def __init__(self):
        super(EditDHCPEvent, self).__init__(
            name='dhcp_edited',
            body={},
            required_acl='events.config.dhcp.edited',
        )
        self.routing_key = 'config.dhcp.edited'
