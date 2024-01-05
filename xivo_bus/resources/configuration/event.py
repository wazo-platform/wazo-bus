# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class LiveReloadEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'live_reload_edited'
    routing_key_fmt = 'config.live_reload.edited'

    def __init__(self, live_reload_enabled: bool):
        content = {'live_reload_enabled': live_reload_enabled}
        super().__init__(content)
