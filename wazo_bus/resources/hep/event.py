# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class HEPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'hep_general_edited'
    routing_key_fmt = 'config.hep_general.edited'

    def __init__(self) -> None:
        super().__init__()
