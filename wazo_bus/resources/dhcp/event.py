# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class DHCPEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'dhcp_edited'
    routing_key_fmt = 'config.dhcp.edited'

    def __init__(self) -> None:
        super().__init__()
