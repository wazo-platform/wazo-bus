# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class DHCPEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'dhcp_edited'
    routing_key_fmt = 'config.dhcp.edited'

    def __init__(self):
        super(DHCPEditedEvent, self).__init__()
