# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class HAEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'ha_edited'
    routing_key_fmt = 'config.ha.edited'

    def __init__(self) -> None:
        super().__init__()
