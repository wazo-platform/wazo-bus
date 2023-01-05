# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class HAEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'ha_edited'
    routing_key_fmt = 'config.ha.edited'

    def __init__(self):
        super().__init__()
