# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class SCCPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'sccp_general_edited'
    routing_key_fmt = 'config.sccp_general.edited'

    def __init__(self) -> None:
        super().__init__()
