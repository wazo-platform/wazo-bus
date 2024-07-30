# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class LocalizationEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'localization_edited'
    routing_key_fmt = 'config.localization.edited'

    def __init__(self) -> None:
        super().__init__()
