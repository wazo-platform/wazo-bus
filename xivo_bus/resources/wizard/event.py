# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class WizardCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'wizard_created'
    routing_key_fmt = 'config.wizard.created'

    def __init__(self) -> None:
        super().__init__()
