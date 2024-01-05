# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent
from .types import RegistrarDict


class RegistrarCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'registrar_created'
    routing_key_fmt = 'config.registrar.created'

    def __init__(self, registrar: RegistrarDict):
        super().__init__(registrar)


class RegistrarDeletedEvent(ServiceEvent):
    service = 'confd'
    name = 'registrar_deleted'
    routing_key_fmt = 'config.registrar.deleted'

    def __init__(self, registrar: RegistrarDict):
        super().__init__(registrar)


class RegistrarEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'registrar_edited'
    routing_key_fmt = 'config.registrar.edited'

    def __init__(self, registrar: RegistrarDict):
        super().__init__(registrar)
