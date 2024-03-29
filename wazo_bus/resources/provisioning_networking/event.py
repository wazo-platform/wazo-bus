# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class ProvisioningNetworkingEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'provisioning_networking_edited'
    routing_key_fmt = 'config.provisioning.networking.edited'

    def __init__(self) -> None:
        super().__init__()
