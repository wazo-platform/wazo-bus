# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class AMIEvent(ServiceEvent):
    service = 'amid'
    name = '{ami_event}'
    routing_key_fmt = 'ami.{name}'

    def __init__(self, ami_event: str, variables: dict[str, str]):
        self.name = type(self).name.format(ami_event=ami_event)
        super().__init__(variables)
