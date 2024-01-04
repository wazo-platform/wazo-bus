# Copyright 2021-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class EmailConfigUpdatedEvent(ServiceEvent):
    service = 'confd'
    name = 'email_config_updated'
    routing_key_fmt = 'config.email.updated'

    def __init__(self) -> None:
        super().__init__()
